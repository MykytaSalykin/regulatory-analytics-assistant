CREATE SCHEMA IF NOT EXISTS finance;

CREATE TABLE IF NOT EXISTS finance.survey_metrics (
    exercise TEXT NOT NULL,
    period TEXT NOT NULL,
    item_code TEXT NOT NULL,
    item_label TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    answer_rank INTEGER,
    source TEXT NOT NULL,
    PRIMARY KEY (exercise, period, item_code, value)
);
