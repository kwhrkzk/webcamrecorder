from . import ISendMail
from ..domain.MailSender import MailSender
from ..domain.Frame import Frame
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime, timedelta


class SendMail(ISendMail.ISendMail):
    def __init__(self) -> None:
        load_dotenv()

        self.sender = MailSender(
            os.getenv("SMTP_SERVER_ADDRESS") or "",
            os.getenv("SMTP_PORT") or "",
            os.getenv("SMTP_ACCOUNT") or "",
            os.getenv("SMTP_PASSWORD") or "")
        self.interval = int(os.getenv("MAIL_INTERVAL_MINUTES") or 1)

        sqlite3.register_converter("DATETIME", sqlite3.converters["TIMESTAMP"])
        self.conn = sqlite3.connect(
            "mydb.db",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cur = self.conn.cursor()
        cur.execute(
            "create table if not exists "
            "mail_histories(date DATETIME primary key)")

    def send(self, frame: Frame, subect: str = "subject", body: str = "body"):
        if not self.sender.can_send:
            return

        cur = self.conn.cursor()

        results = cur.execute(
            "select date from mail_histories order by date desc limit 1")

        item = results.fetchone()

        if item is not None:
            (last_send_date, ) = item
            interval_date = last_send_date + timedelta(minutes=self.interval)
            if datetime.now() <= interval_date:
                return

        self.sender.send(frame, subect, body)
        self.insert_history()

    def insert_history(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "delete from mail_histories where date not in "
            "(select date from mail_histories order by date desc limit 100)")
        cur.execute(
            "insert into mail_histories (date) values (? )",
            (datetime.now(), ))
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
