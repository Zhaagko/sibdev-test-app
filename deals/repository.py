from .models import Deal


def bulk_create_deals(data: list[Deal]):
    Deal.objects.bulk_create(data)


def get_top_spending_customers(limit: int = 5) -> list[Deal]:
    table_name = Deal._meta.db_table
    sql_string = f"""
    WITH TopSpendingCustomers AS (
    SELECT
        customer AS username,
        SUM(total) AS spent_money
    FROM
        {table_name}
    GROUP BY
        customer
    ORDER BY
        spent_money DESC
    LIMIT {limit}
    )

    SELECT
        id,
        tc.username,
        tc.spent_money,
        GROUP_CONCAT(DISTINCT d.item) AS gems
    FROM
        TopSpendingCustomers tc
    JOIN
        {table_name} d
    ON
        tc.username = d.customer
    WHERE
        (
            SELECT
                COUNT(DISTINCT d2.customer)
            FROM
                {table_name} d2
            JOIN
                TopSpendingCustomers tc2
            ON
                tc2.username = d2.customer
            WHERE
                d.item = d2.item
        ) >= 2
    GROUP BY
        tc.username, tc.spent_money
    ORDER BY
        tc.spent_money DESC;
    """
    result = Deal.objects.raw(sql_string)
    return result
