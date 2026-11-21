
import json
import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.modules.file.models import File, FileStatus


DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def process_s3_event(message: dict) -> None:
    detail = message["detail"]

    bucket_name = detail["bucket"]["name"]
    object_key = detail["object"]["key"]
    file_size = detail["object"]["size"]
    etag = detail["object"].get("etag")

    with SessionLocal() as db:
        statement = (
            update(File)
            .where(
                File.bucket_name == bucket_name,
                File.object_key == object_key,
                File.status == FileStatus.PENDING,
            )
            .values(
                file_size=file_size,
                etag=etag,
                status=FileStatus.UPLOADED,
                uploaded_at=datetime.now(timezone.utc),
            )
        )

        result = db.execute(statement)

        if result.rowcount == 0:
            existing_file = db.query(File).filter(
                File.bucket_name == bucket_name,
                File.object_key == object_key,
            ).first()

            if existing_file is None:
                raise ValueError(
                    f"File record not found: {object_key}"
                )

            if existing_file.status == FileStatus.UPLOADED:
                print(f"File already processed: {object_key}")
                return

            raise ValueError(
                f"File cannot be updated: {object_key}"
            )

        db.commit()

    print(f"File uploaded successfully: {object_key}")


def lambda_handler(event, context):
    batch_item_failures = []

    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            process_s3_event(message)

        except Exception as error:
            print(f"Processing failed: {error}")

            batch_item_failures.append({
                "itemIdentifier": record["messageId"]
            })

    return {
        "batchItemFailures": batch_item_failures
    }