Still in initial stage of the project. (data extraction -> transformation (parsing) -> model building -> prediction)

Original purpose of this app is to create a flask API engine which will predict some of the key attributes (tax?sales? etc) on a paper receipt based on the amount/location.
as paper receipts are nondigital, we need to use a tool to convert data on image to digital data which I relied on google ocr api. 
Given an image, ocr returns a json file. I then parsed the json file and return the dimensions that would be used in the modeling.


