## EvaDB Query Parser

This repository contains code for parsing SQL queries and generating English explanations for what these queries are doing. Two main approaches have been explored

- Using local LLMs such as orca-mini-3b with GPT4All and hosted LLMs such as ChatGPT to explain what actions a given query does on the database tables

- Creating a query parser to explain what actions a given query does based on the structure of the query

Both of these approaches have their tradeoffs

The LLM approach is computationally expensive, and slow if using a hosted LLM like ChatGPT due to network calls and compute time. However, it is perhaps more flexible to different types of queries. It may produce erroneous answers.

The parser approach is very fast, as it only relies on structurally decomposing the query. However, it is somewhat inflexible as it only supports a limited number of queries. Generalizing the parser to support arbitrary SQL queries would be akin to writing a SQL compiler, which is well outside the scope of this project.

Very complex queries will prove to be challenging for both LLMs and a parser approach. LLMs likely have not been trained on extremely complex SQL queries, so they not be able to generalize onto those. Writing a parser to handle several levels of nested queries and joins would prove to be extremely challenging.