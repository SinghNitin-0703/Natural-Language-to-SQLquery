from langchain_core.prompts import PromptTemplate

# Few-shot examples
few_shots = [
    {
        'Question': "Find total revenue generated across all transactions.",
        'SQLQuery': "SELECT ROUND(SUM(Total), 2) AS total_revenue FROM walmart_sales;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The total revenue across all transactions is calculated by summing the Total column."
    },
    {
        'Question': "Count the total number of sales transactions per branch.",
        'SQLQuery': "SELECT Branch, COUNT(`Invoice ID`) AS total_transactions FROM walmart_sales GROUP BY Branch;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The number of transactions per branch is found by counting Invoice IDs grouped by Branch."
    },
    {
        'Question': "Calculate average customer rating per product line.",
        'SQLQuery': "SELECT `Product line`, ROUND(AVG(Rating), 2) AS avg_rating FROM walmart_sales GROUP BY `Product line`;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The average rating per product line is calculated by averaging Rating grouped by Product line."
    },
    {
        'Question': "Find the number of transactions done using each payment method.",
        'SQLQuery': "SELECT Payment, COUNT(*) AS total_payments FROM walmart_sales GROUP BY Payment;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The number of transactions per payment method is found by counting and grouping by Payment."
    },
    {
        'Question': "Retrieve total quantity sold for each product line.",
        'SQLQuery': "SELECT `Product line`, SUM(Quantity) AS total_quantity FROM walmart_sales GROUP BY `Product line`;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The total quantity sold per product line is calculated by summing Quantity grouped by Product line."
    },
    {
        'Question': "Find average revenue per transaction for each branch.",
        'SQLQuery': "SELECT Branch, ROUND(SUM(Total)/COUNT(`Invoice ID`), 2) AS avg_revenue_per_txn FROM walmart_sales GROUP BY Branch;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The average revenue per transaction for each branch is calculated by dividing total sales by transaction count."
    },
    {
        'Question': "Determine which product line has the highest total sales in each city.",
        'SQLQuery': "SELECT City, `Product line`, SUM(Total) AS total_sales FROM walmart_sales GROUP BY City, `Product line` ORDER BY City, total_sales DESC;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Product lines with highest sales per city are found by grouping by City and Product line, then ordering by total sales."
    },
    {
        'Question': "Calculate monthly total sales trend.",
        'SQLQuery': "SELECT DATE_FORMAT(STR_TO_DATE(Date, '%Y-%m-%d'), '%Y-%m') AS month, SUM(Total) AS total_sales FROM walmart_sales GROUP BY month ORDER BY month;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Monthly sales trend is calculated by extracting month from Date and summing Total for each month."
    },
    {
        'Question': "Find top 3 most popular product lines by number of transactions.",
        'SQLQuery': "SELECT `Product line`, COUNT(*) AS transactions FROM walmart_sales GROUP BY `Product line` ORDER BY transactions DESC LIMIT 3;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The top 3 most popular product lines are found by counting transactions and limiting to top 3."
    },
    {
        'Question': "Compare average gross income of male vs. female customers.",
        'SQLQuery': "SELECT Gender, ROUND(AVG(`gross income`), 2) AS avg_gross_income FROM walmart_sales GROUP BY Gender;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Average gross income by gender is calculated by grouping by Gender and averaging gross income."
    },
    {
        'Question': "Find top-performing product line per city using ranking.",
        'SQLQuery': "SELECT City, `Product line`, SUM(Total) AS total_revenue, RANK() OVER (PARTITION BY City ORDER BY SUM(Total) DESC) AS rank_in_city FROM walmart_sales GROUP BY City, `Product line`;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Top-performing product lines per city are identified using window functions with RANK to partition by City."
    },
    {
        'Question': "Identify the hour of the day with the highest total sales for each branch.",
        'SQLQuery': "SELECT Branch, HOUR(STR_TO_DATE(Time, '%H:%i:%s')) AS hour_of_day, SUM(Total) AS total_sales FROM walmart_sales GROUP BY Branch, hour_of_day ORDER BY Branch, total_sales DESC;",
        'SQLResult': "Result of the SQL query",
        'Answer': "The busiest hour per branch is found by extracting hour from Time and summing sales grouped by Branch and hour."
    },
    {
        'Question': "Calculate revenue contribution percentage by gender and customer type.",
        'SQLQuery': "SELECT Gender, `Customer type`, ROUND(SUM(Total) * 100 / (SELECT SUM(Total) FROM walmart_sales), 2) AS revenue_percent FROM walmart_sales GROUP BY Gender, `Customer type` ORDER BY revenue_percent DESC;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Revenue contribution percentage is calculated by dividing group total by overall total and multiplying by 100."
    },
    {
        'Question': "Compute monthly sales growth rate percentage over previous month.",
        'SQLQuery': "SELECT DATE_FORMAT(STR_TO_DATE(Date, '%Y-%m-%d'), '%Y-%m') AS month, SUM(Total) AS total_sales, ROUND((SUM(Total) - LAG(SUM(Total)) OVER (ORDER BY DATE_FORMAT(STR_TO_DATE(Date, '%Y-%m-%d'), '%Y-%m'))) / LAG(SUM(Total)) OVER (ORDER BY DATE_FORMAT(STR_TO_DATE(Date, '%Y-%m-%d'), '%Y-%m')) * 100, 2) AS growth_percent FROM walmart_sales GROUP BY month ORDER BY month;",
        'SQLResult': "Result of the SQL query",
        'Answer': "Monthly growth rate is calculated using LAG window function to compare current month sales with previous month."
    },
]

# MySQL prompt
mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.

Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.

Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.

Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: SQL Query to run (without any markdown formatting or code blocks)
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only provide the SQL query without any additional text, explanations, or markdown code blocks.
"""

# Example prompt template
example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
)