# KSB API Documentation

This API allows users to retrieve a list of all KSBs, filter KSBs by type, add new KSBs, update existing KSBs, and delete KSBs.


## Endpoints  

### **GET all KSBs**  
- **Endpoint:** `GET /ksbs`  
- **Response:** `200 OK` (returns a list of all KSBs) 
- **Error Response** 
  `500 Internal Server Error`

### **GET all knowledge KSBs**  
- **Endpoint:** `GET /ksbs/knowledge`  
- **Response:** `200 OK` (returns a list of all knowledge KSBs)  
- **Error Response** 
  wrong endpoint - `404 endpoint does not exist`
  internal error - `500 Internal Server Error`


### **GET all skill KSBs**  
- **Endpoint:** `GET /ksbs/skill`  
- **Response:** `200 OK` (returns a list of all skill KSBs)  
- **Error Response** 
  wrong endpoint - `404 endpoint does not exist`
  internal error - `500 Internal Server Error`


### **GET all behaviour KSBs**  
- **Endpoint:** `GET /ksbs/behaviour`  
- **Response:** `200 OK` (returns a list of all behaviour KSBs) 
- **Error Response** 
  wrong endpoint - `404 endpoint does not exist`
  internal error - `500 Internal Server Error`


### **GET a specific KSB by UUID**  
- **Endpoint:** `GET /ksbs/{uuid}`  
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Response:** `200 OK` (returns the requested KSB)  
- **Error Response** 
  wrong endpoint - `404 endpoint does not exist`
  internal error - `500 Internal Server Error`


### **POST a new KSB**  
- **Endpoint:** `POST /ksbs/{type}` (`type` must be `knowledge`, `skill`, or `behaviour`)  
- **Payload:**   (`theme` must be `code quality`, `meeting user needs`, `the ci cd pipeline`, `refreshing and patching`, `operability`, `data persistence`, `automation`, `data security`)

  ```json
  {
    "code": 12,
    "description": "Automate tasks where it introduces improvements to the efficiency of business processes and reduces waste, considering the effort and cost of automation.",
    "theme": "meeting user needs"
  }
- **Response:** `201 OK`
- **Error Response** 
  wrong endpoint - `404 endpoint does not exist`
  duplicate kSB - `409 Ksb already exists in database`
  invalid type - `400 - "type" is not a valid ksb_type`
  invalid code - `400 - "code" is not a valid ksb code, choose an int from 1 to 50`
  invalid description - `400 - description needs to be more than 15 characters and less than 300 characters in length`
  internal error - `500 Internal Server Error`


### **DELETE a specific KSB by UUID** 
- **Endpoint:** `DELETE /ksbs/{uuid}`
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Response:** `204 NO CONTENT`
- **Error Response** 
    ksb doesnt exist - `404 ksb cannot be deleted as it does not exist in database`
    invalid uuid - `404 uuid is invalid`
    internal error - `500 Internal Server Error`



### ••UPDATE/PUT a ksb**
- **Endpoint:** `PUT /ksbs/{uuid}`
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Payload:** (`payload` can include `type` and/or `code` and/or `description`, and/or `is_complete`)
```json
{
  "type": "knowledge", 
  "code": 12,
  "is_complete": true
}
```
- **Response:** `204 OK`
- **Error Response** 
    invalid type - `400 - "type" is not a valid ksb_type`
    invalid code - `400 - "code" is not a valid ksb code, choose an int from 1 to 50`
    invalid description - `400 - description needs to be more than 15 characters and less than 300 characters in length`
    invalid is_complete - `400 - is_complete must be a boolean (true or false)`
    ksb doesnt exist - `404 ksb with that uuid does not exist in database`
    invalid uuid - `404 uuid is invalid`
    internal error - `500 Internal Server Error`
