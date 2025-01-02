import logging

import psycopg2


def track_performance(decision_source, signal_value, trade_outcome, trading_performance=None):
    """
    Log performance metrics into a PostgreSQL database.
    :param decision_source: Source of the decision (e.g., "ML" or "Rules").
    :param signal_value: Signal score used for the decision.
    :param trade_outcome: Outcome of the trade (e.g., "profit" or "loss").
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname= trading_performance,
            user= trading_user,
            password= SQLPW,  # Replace with your PostgreSQL password
            host= 20.2.84.42
        )
        cursor = conn.cursor()

        # Insert performance data
        insert_query = INSERT INTO trade_performance (decision_source, signal_value, trade_outcome)
        VALUES (%s, %s, %s)

        cursor.execute(insert_query, (decision_source, signal_value, trade_outcome))
        conn.commit()

        logging.info(Logged performance: {decision_source}, var = {signal_value}, {trade_outcome}
        )

        # Close connection
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error logging performance data: {e}")
