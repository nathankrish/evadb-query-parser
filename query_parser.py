from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
import re

class ExplainSQL(AbstractFunction):
    @property
    def name(self) -> str:
        return "explainSQL"
    
    @forward()
    def parse_sql(self, query: str) -> str:
        tokens = re.split(r'[ ,]', query)
        tokens = [item for item in tokens if item]
        command = tokens[0]
        if (command == "SELECT"):
            return self.parse_select(tokens)
        elif (command == "INSERT"):
            return self.parse_insert(tokens)
        else:
            return ""
        
    def parse_select(self, tokens: list[str]) -> str:
        try :
            end_cols = tokens.index("FROM")
        except:
            return "The given SELECT query is malformed. It does not have a FROM clause."

        res = self.handle_columns(tokens, end_cols)

        try:
            start_where = tokens.index("WHERE")
            res += '\n' + self.handle_where(tokens, start_where)
        except:
            res = res
        
        try:
            start_group = tokens.index("GROUP")
            res += '\n' + self.handle_group(tokens, start_group)
        except:
            res = res

        try:
            start_order = tokens.index("ORDER")
            res += '\n' + self.handle_order(tokens, start_order)
        except:
            res = res
        
        return res

    def handle_where(tokens: list[str], start_where: int) -> str:
        
        end_where = start_where
        while (end_where < len(tokens) and tokens[end_where] != "GROUP" and tokens[end_where] != "ORDER"):
            end_where += 1
        where_tokens = tokens[start_where: end_where]
        res = 'The query filters on the conditions: '
        for i in range(1, len(where_tokens) - 1):
            if (where_tokens[i] == '='):
                res += where_tokens[i-1]
                res += ' = '
                res += where_tokens[i+1]
                if (i < len(where_tokens) - 2):
                    res += ", "
        res += "."
        return res

    def handle_group(tokens: list[str], start_group: int) -> str:
        
        end_group = start_group
        while (end_group < len(tokens) and tokens[end_group] != "ORDER"):
            end_group += 1
        group_tokens = tokens[start_group: end_group]
        if (len(group_tokens) <= 3):
            res = 'The query groups on the ' 
            res += group_tokens[2]
            res += ' column.'
            return res
        else:
            res = 'The query groups on the columns: '
            for i in range(2, len(group_tokens)):
                res += group_tokens[i]
                if i < len(group_tokens) - 1:
                    res += ", "
            res += "."
            return res

    def handle_order(tokens: list[str], start_order: int) -> str:
        order_tokens = tokens[start_order:]
        if (len(order_tokens) <= 3):
            res = 'The query orders on the '
            res += order_tokens[2]
            res += ' column.'
            return res
        else:
            res = 'The query orders on the columns: '
            for i in range(2, len(order_tokens)):
                res += order_tokens[i]
                if i < len(order_tokens) - 1:
                    res += ", "
            res += "."
            print(res)
            return res
        
    def parse_insert(tokens: list[str]) -> str:
        if (len(tokens) < 3):
            return "The given INSERT query is malformed. It does not specify a table."
        table_name = tokens[2]

        end_cols = tokens.index("VALUES")
        cols = tokens[3:end_cols]
        cols = list(map(lambda x: x.strip('(').strip(')').strip(','), cols))
        
        vals = tokens[end_cols+1:]
        vals = list(map(lambda x: x.strip('(').strip(')').strip(','), vals))
        
        tupString = ""
        for i in range(len(cols)):
            tupString += (cols[i] + ": " + vals[i])
            if (i != len(cols) - 1):
                tupString += ", "
        
        return f"The given INSERT query inserts a tuple with {tupString} into the {table_name} table."

    def handle_columns(tokens: list[str], end_cols: int) -> str:
        cols = tokens[1:end_cols]
        tables = tokens[end_cols+1:]

        cols = list(map(lambda x: x.strip().strip(","), cols))

        if len(cols) == 0:
            return f"The given SELECT query is malformed. It does not specify any columns."
        if (cols[0] == "*"):
            return f"The given query selects all columns from the {tables[0]} table."
        else:
            col_names = []
            res_names = []

            isColName = True
            for s in cols:
                if (s != "AS"):
                    if isColName:
                        col_names.append(s)
                    else:
                        res_names.append(s)
                    isColName = not isColName

            if len(col_names) == 1:
                return f"The given query selects the {col_names[0]} column as {res_names[0]} from the {tables[0]} table."
            else:
                return f"The given query selects the {'(' + ', '.join(col_names) + ')'} columns as {'(' + ', '.join(res_names) + ')'} from the {tables[0]} table."