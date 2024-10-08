import csv
from io import StringIO

from fastapi import status, UploadFile, HTTPException, APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from ..sql_alchemy.database import get_db

router = APIRouter(tags=['image'], prefix='/v1')


@router.post("/upload-file")
async def load_upload_file(background_tasks: BackgroundTasks, file: UploadFile | None = None,
                           db: Session = Depends(get_db)):
    if not file:
        ## raise exception when no file is uploaded
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No upload file sent")
    else:
        ## raise exception when upload file is not in csv format
        if file.content_type not in ['text/csv']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document type")

        ## Validate CSV format
        try:
            content = await file.read()
            stream = StringIO(content.decode("utf-8"))
            reader = csv.DictReader(stream)
            products = []
            for row in reader:
                # print(row)
                serial_num = row.get('Serial Number')
                product_name = row.get('Product Name')
                input_urls = row.get('Input Image Urls').split(',')
                products.append((int(serial_num), product_name, input_urls))
            stream.close()
            file.file.close()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"uploaded Csv format is invalid")

        background_tasks.add_task()
        background_tasks.tasks()
        print(products)
        return {"filename": file.filename}
