# Database Models
---

### Error  
Used to store errors that occur during the manufacturing process. This is used to track errors and find root causes for future improvements and build prevention into our process.  

**Keys:**  
- **id** - `int` - Primary key  
- **part_number** - `string` - Part number (Not all part numbers are integers)  
- **description** - `string` - Description of the error  
- **machine** - `string` - Machine that the error occurred on (Can be empty if not machine specific)  
- **root_cause** - `string` - Root cause of the error if found  
- **notes** - `string` - Notes about the error that can be added to any time  
- **name** - `string` - Name of person who reported the error for tracking purposes  
- **date** - `date` - Date the error was reported   
  <br>
  
  `
  Sample repr-> <Error #: 5, Date: 12/15/2022, Description: Machine punched holes on edge of sheet>
  `
---
### File  
Used to store file info that are uploaded to the AWS S3 Bucket. Mainly used to structure the page so we can make the correct
calls to the AWS S3 Bucket when fetching files/building presigned urls/etc. If file is linked to an error, the error id will be stored in the error_id column.

**Keys:**  
- **id** - `int` - Primary key  
- **file_name** - `string` - Name of the file  
- **error_id** - `int` - Error id that the file is linked to from errors table  
- **version** - `string` - Version of the file. This is to maintain version control of files in S3 Bucket  
- **presigned_url** - `string` - Presigned url to the file in S3 Bucket to allow downloads without further authentication  
  <br>

  `
  Sample repr-> <File: ID:2, Name:problem1.jpg, Error ID: 3, Version: uj5o.4VGlKcoUZAWIdu5UOqq>
  `

---
### Material  
Used to store materials used in our manufacturing process.  
  
**Keys:**  
- **id** - `int` - Primary key  
- **gauge** - `int` - Gauge of the material  
- **material_name** - `string` - Name of the material  
- **blanks** - `ORM Object` - List of blanks that are in our inventory of this material type  
  <br>

  `
    Sample repr-> <Material: ID: 1, Gauge: 18, Material Name: AZ>  
  `

---
### Blank
Used to store blanks of a material. This is used to track the inventory of blanks and the sizes of the blanks.  

**Keys:**  
- **id** - `int` - Primary key  
- **material_id** - `int` - Foreign key linked to materials table  
- **length** - `Integer` - Length of the blank  
- **width** - `Integer` - Width of the blank  
- **quantity** - `Integer` - Quantity of the blank  
- **material** - `ORM Object` - Material object that the blank is linked to  
  <br>

  `
    Sample repr-> <Blank: ID: 1, Material Name: AZ, Length: 96, Width: 5, Quantity: 10>  
  `

---
### Sizes
Store sheet sizes for the different materials  

**Keys:**  
- **id** - `int` - Primary key  
- **material_id** - `int` - Foreign key linked to materials table  
- **length** - `Integer` - Length of the blank  
- **width** - `Integer` - Width of the blank  
  <br>

  `
    Sample repr-> <Size: Material ID: 1, Material Name: AZ, Length: 48, Width: 96>  
  `

---
### Nest  
Used to store machine nesting information for the lasers and punch press. Useful for ensuring nests are the same between machines.  
  
**Keys:**  
- **id** - `int` - Primary key  
- **nest_name** - `string` - Name of the nest  
- **nested_with** - `string` - Lists parts nested. Future want: Link to parts table  
- **sheet_x** - `float` - X dimension of the sheet  
- **sheet_y** - `float` - Y dimension of the sheet  
- **scrap** - `float` - Scrap percentage of the nest  
- **punch_forming** - `boolean` - Punch press using forming tool on this nest  
- **clamp_position_change** - `boolean` - Punch press clamp position change on this nest  
- **setup_time** - `float` - Setup time for the nest or part when forming  
- **process_time** - `float` - Process time for the nest or part when forming  
- **date** - `date` - Date the nest was created  
- **machine_id** - `int` - Machine id that the nest was created on from machines table  
- **material_id** - `int` - Material id that the nest was created on from materials table  
  <br>
    
  `
    Sample repr-> <Nest #: N174743, Material ID: 5, Machine ID: 2, Date: 12/7/2022>
  `

---
### Machine
Stores different machines, Lasers, Punch Press, etc.  

**Keys:**  
- **id** - `int` - Primary key  
- **name** - `string` - Name of the machine  
- **machine_type** - `string` - Type of machine  
  <br>
  
    `
      Sample repr-> <Machine Name: Amada Laser , Type: Laser>  
    `

---
### Part  
Used to store a part originating from an ECO that has been released.  
  
**Keys:**  
- **id** - `int` - Primary key  
- **eco_number** - `string` - ECO number that the part was released from  
- **part_number** - `string` - Part number. Sometimes contains letters  
- **description** - `string` - Description of the part from ECO  
- **revision** - `int` - Revision number of the part  
- **measuring_unit** - `string` - Measuring unit of the part that defaults to 'EA'  
- **item_type** - `string` - Item type of the part from ECO  
- **material_code** - `string` - Material code of the part from ECO that defaults to 'M' for manufactured part  
- **replaces** - `string` - Replaces current part listed  
- **material_disposition** - `string` - Material disposition of the part from ECO. Maybe a future table?  
- **effectivity_date** - `string` - Effectivity date of the part from ECO. Not always a date. Needs standardized with actual date format  
- **continue_to_buy** - `string` - Continue to buy of the part from ECO  
- **comments** - `string` - Comments of the part from ECO that usually lists material or changes made on rev up  
- **amada** - `string` - Part nested on Amada Laser  
- **trumpf** - `string` - Part nested on Trumpf Laser  
- **punch** - `string` - Part nested on Punch Press  
- **forming** - `string` - Part program created for forming machines  
- **status** - `string` - Status of the part. Can be 'Released' or 'Pending'  
- **added** - `date` - Date the part was added to the database  
  <br>

  `
    Sample repr-> <Part #: 123456, Rev: 2, ECO#: 2355>  
  `

---
### Request  
Used to store requests for parts to be made, or nests to be created/modified.  

**Keys:**  
- **id** - `int` - Primary key  
- **to_change** - `string` - Part number that is being changed or nest that is being created/modified  
- **description** - `string` - Description of the request  
- **request_type** - `string` - Type of request. Can be 'Part Request', 'Laser Change' or 'Forming Change'  
- **requested_by** - `string` - Name of the person who requested the change for tracking purposes  
- **date** - `date` - Date the request was made  
- **date_completed** - `date` - Date the request was completed. Request will still show for 5 days after completion    
  <br>

  `
    Sample repr-> <Request #: 1, What to Change: N174743, Description: Add 999999 as filler, Requester: Alex, Type: Laser Change>
  `

---
### Machine  
Used to store machine information.  
  
**Keys:**  
- **id** - `int` - Primary key  
- **name** - `string` - Name of the machine  
- **machine_type** - `string` - Type of machine. Can be 'Laser', 'Punch', or 'Forming'  
  <br>  
  
  `
    Sample repr-> <Machine: ID: 1, Name: Salvagnini, Type: Forming>
  `

---
### User
Stores user information  

**Keys:**  
- **id** - `int` - Primary key  
- **first_name** - `string` - First name of the user  
- **last_name** - `string` - Last name of the user  
- **email** - `string` - Email of the user. Must be unique  
- **password** - `string` - Password of the user  
- **isadmin** - `boolean` - Is the user an admin  
  <br>

  `
    Sample repr-> '<User #: ID: 1, First Name: Alex, Last Name: Smith, Email: asmith@bluestarcooking.com>'
  `

---
### Project
Stores project information  

**Keys:**  
- **id** - `int` - Primary key  
- **created** - `date` - Date the project was created  
- **updated** - `date` - Date the project was last updated  
- **updated_by** - `string` - Name of the user who last updated the project  
- **completed** - `date` - Date the project was completed  
- **user_name** - `string` - Name of the user who created the project  
- **project_name** - `string` - Name of the project  
- **project_type** - `string` - Type of project  
- **product_line** - `string` - Product line of the project  
- **eco** - `string` - ECO number of the project  
- **notes** - `string` - Notes for the project  
- **date_requested** - `date` - Projected completion date or requested completion  
- **progress** - `Integer` - Progress of the project  
- **late** - `boolean` - Project late status. This is unused with addition of datetime module logic  
- **status** - `string` - Status of the project. Can be 'Incomplete' or 'Completed'  
  <br>

  `
    Sample repr-> '<Project #: ID: 1, Name: Project 1, Owner: Alex Smith, Created: 12-15-1990, Updated: 12-16-1990, Completed : None>'
  `

---
### ProtoPart
Stores proto part information  

**Keys:**  
- **id** - `int` - Primary key  
- **part_number** - `string` - Part number of the proto part  
- **description** - `string` - Description of the proto part  
- **updated_by** - `string` - Name of the user who last updated the proto part  
- **project_id** - `int` - Foreign key to project table  
- **material** - `string` - Material of the proto part  
- **processes** - `string` - Processes of the proto part. Is unused with addition of individual proccesses to this table.  
- **bin_location** - `string` - Bin location of the proto part  
- **notes** - `string` - Notes for the proto part  
- **status** - `string` - Status of the proto part. Can be 'Incomplete' or 'Completed'  
- **punch** - `boolean` - Punch needed?  
- **form** - `boolean` - Form needed?  
- **weld** - `boolean` - Weld needed?  
- **polish** - `boolean` - Polish needed?  
- **paint** - `boolean` - Paint needed?  
- **assembly** - `boolean` - Assembly needed?  
- **enamel** - `boolean` - Enamel needed?  
- **fav** - `boolean` - FAV needed?  
- **other** - `boolean` - Other needed?  
- **punch_status** - `boolean` - Punch Complete?  
- **form_status** - `boolean` - Form Complete?  
- **weld_status** - `boolean` - Weld Complete?  
- **polish_status** - `boolean` - Polish Complete?  
- **paint_status** - `boolean` - Paint Complete?  
- **assembly_status** - `boolean` - Assembly Complete?  
- **enamel_status** - `boolean` - Enamel Complete?  
- **fav_status** - `boolean` - FAV Complete?  
- **other_status** - `boolean` - Other Complete?  
- **files** - `ORM object` - ORM object for files associated with the proto part  
  <br>

  `
    Sample repr-> '<ProtoPart #: ID: 1, Part #: 123456, Description: Part 1, Project: Project 1, Status: Incomplete>'
  `

---
### ProtoFile
Stores proto file information  

**Keys:**  
- **id** - `int` - Primary key  
- **file_name** - `string` - Name of the file  
- **version** - `string` - Version of the file  
- **description** - `string` - Description of the file  
- **updated** - `date` - Date the file was last updated  
- **updated_by** - `string` - Name of the user who last updated the file  
- **project_id** - `int` - Foreign key to project table  
- **part_id** - `int` - Foreign key to proto part table  
- **notes** - `string` - Notes for the file  
