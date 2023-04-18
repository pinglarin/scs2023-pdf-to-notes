#### Front end stuff
1. Create a js component to handle file uploads (called FileUploader.js) by using file uploader code https://www.spguides.com/upload-file-in-react-js/ and use DragUploader.js as reference
2. {unused atm} Created DragAndDrop.js to handle drag and drop files instead of clicking a button to upload a file. However, it is hard to integrate the submit function of the normal file upload to the drag and drop one, so this is not used yet, and currently the normal file upload is used.
3. Create a FastAPI function to handle file upload via http://localhost:8000/gen_summary/
In main.py (main FastAPI file)  [Create a temporary storage on Server aka FastAPI to store the file while being processed]
4. Adjust FileUploader.js (temporarily TempUploader.js) to be like DragUploader.js.
5. decorate Uploader Page
6. Extract text from uploaded file, which is a SpooledTemporaryFile
https://stackoverflow.com/questions/47171154/how-do-i-decode-text-from-a-pdf-online-with-requests used something sort of like this
7. Convert output text into word file
>> not sure if this can be done because the most possible way to return a file is using FileResponse
but it requires a path to the file and probably cant send a file that has been generated in the function. 
Will probably have to result to simply sending a string to the user.
8. display the summarized text on the web page <<< To Be DONE

***TO BE DONE***
Fill in generator function

Resources
https://fastapi.tiangolo.com/tutorial/request-files/
