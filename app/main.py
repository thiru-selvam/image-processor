from fastapi import FastAPI, File, status, UploadFile, HTTPException
import csv
from io import StringIO # new import

app = FastAPI(title='Image Processor from CSV')

@app.get('/')
async def home_url():
    return {'message':'This is home URL page'}

@app.post("/upload-file/")
async def load_upload_file(file: UploadFile | None = None):
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
                print(row)
                product_name = row.get('Product Name')
                input_urls = row.get('Input Image Urls').split(',')
                products.append((product_name, input_urls))
            stream.close()
            file.file.close()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"uploaded Csv format is invalid")

        print(products)
        return {"filename": file.filename}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
