#### Front end stuff
1. Create a js component to handle file uploads (called FileUploader.js) by using file uploader code https://www.spguides.com/upload-file-in-react-js/ and use DragUploader.js as reference
2. {unused atm} Created DragAndDrop.js to handle drag and drop files instead of clicking a button to upload a file. However, it is hard to integrate the submit function of the normal file upload to the drag and drop one, so this is not used yet, and currently the normal file upload is used.
3. Create a FastAPI function to handle file upload via http://localhost:8000/gen_summary/
In main.py (main FastAPI file)  [Create a temporary storage on Server aka FastAPI to store the file while being processed]
4. Adjust FileUploader.js (temporarily TempUploader.js) to be like DragUploader.js.
5. decorate Uploader Page

***TO BE DONE***
Fill in generator function