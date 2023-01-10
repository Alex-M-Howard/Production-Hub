## Routes
#### /  
###### **GET** -> Returns homepage with at-a-glance information  
  
<br>

#### /nesting_calculator  
###### **GET** -> Returns nesting calculator page for routing help and/or nesting estimates  

<br>

#### /blanks/inventory  
###### **GET** -> Returns page with all blanks from database and also form to add new blanks  
###### **POST** -> Adds new blank to database  
###### **DELETE** -> Deletes blank from database  

<br>

#### /eco  
###### **GET** -> Returns page with all parts from database with filters to sort/search for parts

<br>

#### /data_explorer  
###### **GET** -> Returns page with nests for all machines from database with filters to sort/search for nests  


<br>


#### /amada/  
###### **GET** -> Returns page with links to other Amada routes  

<br> 

#### /amada/blankcam  
###### **GET** -> Returns page with SOP for Amada 3i software BlankCAM  

<br>

#### /amada/data_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software DataExplorer  

<br>

#### /amada/material_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software MaterialExplorer  

<br>

#### /amada/parameter_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software ParameterExplorer  

<br>

 
#### /trumpf/  
###### **GET** -> Returns page with links to other Trumpf routes  

<br> 

#### /trumpf/trutops  
###### **GET** -> Returns page with SOP for Trumpf TruTops software  

<br>

#### /trumpf/offline_loading  
###### **GET** -> Returns page with SOP for Trumpf Offline Loading of programs  

<br>


#### /punch/  
###### **GET** -> Returns page with links to other Punch routes  

<br> 

#### /punch/sop  
###### **GET** -> Returns page with SOP for Punch Press software  

<br>

 
#### /forming/  
###### **GET** -> Returns page with links to other Forming routes  

<br> 

#### /forming/salvagnini_guide  
###### **GET** -> Returns page with manual for Salvagnini software  

<br>

#### /forming/bend_operation  
###### **GET** -> Returns page with manual for Bend Operation on Amada machine  

<br>

#### /forming/bend_parameters  
###### **GET** -> Returns page with manual for Bend Parameters on Amada machine  

<br> 

#### /forming/users_guide  
###### **GET** -> Returns page with manual for Users Guide on Amada machine  

<br>

#### /forming/data_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software DataExplorer  

<br>

#### /forming/material_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software MaterialExplorer  

<br>

#### /forming/parameter_explorer_sop  
###### **GET** -> Returns page with manual for Amada 3i software ParameterExplorer  

<br>


#### /errors/  
###### **GET** -> Returns page with error log

<br>

#### /errors/add  
###### **GET** -> Returns page with form to add new error  
###### **POST** -> Adds new error to database  

<br>

#### /errors/:id  
###### **GET** -> Returns page with error details


<br>

#### /errors/edit/:id  
###### **GET** -> Returns page with form to edit error  
###### **POST** -> Edits error in database  

<br>

#### /errors/:id/add  
###### **GET** -> Returns page with form to add images to error  
###### **POST** -> Adds images to error in database and sends file to AWS S3 Bucket  


<br>


#### /requests/  
###### **GET** -> Returns page with all requests from database  
###### **POST** -> Adds new request to database  
###### **DELETE** -> Signals deletion countdown of request. Actually removed in GET route once 5 days have passed. Authorization needed  

<br>

#### /users/signup  
###### **GET** -> Returns page with form to create new user  
###### **POST** -> Creates new user in database with temporary password and sends email to user with link to reset password  

<br>

#### /users/verification  
###### **GET** -> Returns page with form to verify user  
###### **POST** -> Verifies user in database. Redirects to change password  

<br>

#### /users/login  
###### **GET** -> Returns page with form to login user  
###### **POST** -> Verifies user in database. Logs in and redirects to dashboard  

<br>

#### /users/logout  
###### **GET** -> Logs out user and redirects to login page  

<br>

#### /users/change-password  
###### **GET** -> Returns page with form to change password  
###### **POST** -> Changes password in database  

<br>

#### /proto/  
###### **GET** -> Returns dashboard that is being used as homepage  

<br>

#### /proto/all_projects  
###### **GET** -> Returns page with all projects listed  

<br>

#### /proto/createProject  
###### **GET** -> Returns page with form to create new project  
###### **POST** -> Creates new project in database  

<br>

#### /proto/:project_name  
###### **GET** -> Returns page with project details  

<br>

#### /proto/:project_name/edit  
###### **GET** -> Returns page with form to edit project details  
###### **POST** -> Edits project details in database  

<br>

#### /proto/:project_name/create_part  
###### **GET** -> Returns page with form to create new part  
###### **POST** -> Creates new part in database  

<br>

#### /proto/:project_name/:part_number  
###### **GET** -> Returns page with part details  

<br>

#### /proto/:project_name/:part_number/edit  
###### **GET** -> Returns page with form to edit part details  
###### **POST** -> Edits part details in database  

<br>

#### /proto/:project_name/:part_number/add_file  
###### **GET** -> Returns page with form to add file to part  
###### **POST** -> Uploads file to AWS S3 Bucket and adds file info to database  

<br>

#### /proto/:project_name/:part_number/:file_name/versions  
###### **GET** -> Returns page with all versions of a file for download   

<br>

#### /proto/my_projects  
###### **GET** -> Returns page with my projects   

<br>

#### /proto/update_process  
###### **POST** -> Updates process of part in database with True/False   

<br>


#### /blanks/data  
###### **GET** -> Returns all blanks in the database sorted by material_id in JSON format  

<br> 

#### /materials/data  
###### **GET** -> Returns all materials in the database in JSON format  

<br>

#### /eco/data  
###### **GET** -> Returns all parts in the database in JSON format  

<br>

#### /eco/data/obsolete  
###### **GET** -> Returns all obsolete parts in the database in JSON format  

<br>

#### /amada/data  
###### **GET** -> Returns all parts nested on Amada in the database in JSON format  

<br>

#### /trumpf/data  
###### **GET** -> Returns all parts nested on Trumpf in the database in JSON format  

<br>

#### /punch/data  
###### **GET** -> Returns all parts nested on Punch Press in the database in JSON format  

<br>

#### /forming/data  
###### **GET** -> Returns all parts nested on Forming Machines in the database in JSON format  

<br>

#### /errors/data  
###### **GET** -> Returns all errors in the database in JSON format  

<br>

#### /get_all_projects_incomplete  
###### **GET** -> Returns all projects in the database that are incomplete as ORM objects  

<br>

#### /get_all_projects_complete  
###### **GET** -> Returns all projects in the database that are complete as ORM objects  

<br>

#### /get_my_projects_incomplete  
###### **GET** -> Returns my projects in the database that are incomplete as ORM objects  

<br>

#### /get_my_projects_complete  
###### **GET** -> Returns my projects in the database that are complete as ORM objects  

<br>
