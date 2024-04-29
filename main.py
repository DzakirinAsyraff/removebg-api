import io
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import base64

app = FastAPI()

# TO RUN: uvicorn main:app --reload

# @app.post("/removebg")
# def removeImageBackground(image: bytes):
#     output = remove(image)
#     # print(output)
#     return output

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/removebgimg")
async def removeBackgroundFile(file: UploadFile = File(...)):
    
    request_object_content = await file.read()
    input_img = Image.open(io.BytesIO(request_object_content))
    # # Read the image file
    # input_img = await file.read()
    
    

    # Use Rembg to remove the background
    rembg_image = remove(input_img)
    
    # crop the image
    bbox = rembg_image.getbbox()
    output_cropped = rembg_image.crop(bbox)
    
    # resize the image
    new_size = (1000, 1000)
    if(output_cropped.width > new_size[0] or output_cropped.height > new_size[1]):
    
        # Calculate the ratio
        ratio = min(new_size[0]/output_cropped.width, new_size[1]/output_cropped.height)

        # Calculate the new width and height
        new_width = int(output_cropped.width * ratio)
        new_height = int(output_cropped.height * ratio)

        print("old crop", output_cropped.width, output_cropped.height)

        print("new crop", new_width, new_height)

        final = output_cropped.resize((new_width, new_height))

    else:
        final = output_cropped
    
    final_bytes_io = io.BytesIO()
    final.save(final_bytes_io, format='PNG')
    final_bytes = final_bytes_io.getvalue()

    # Return the processed image data
    # return StreamingResponse(output_image, media_type="image/png")
    
    return Response(content=final_bytes, media_type="image/png")


@app.post("/removebgbyt")
def removeBackgroundByte(image: str):
    # Decode the base64 encoded image data
    image_bytes = base64.b64decode(image)

    # # Load the image using Rembg's imread
    # input_image = imread(image_bytes)

    # Use Rembg to remove the background
    output_image = remove(image_bytes)

    # # Save the processed image to a BytesIO object
    # output_buffer = io.BytesIO()
    # imsave(output_buffer, output_image, format="png")
    # output_buffer.seek(0)

    # Encode the processed image to base64
    # processed_image_base64 = base64.b64encode(output_image.getvalue()).decode('utf-8')

    # Return the processed image data
    return {"processed_image": output_image}
