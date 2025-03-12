# KSB API Documentation

This API allows users to retrieve a list of all KSBs, filter KSBs by type, add new KSBs, update existing KSBs, and delete KSBs.


## Endpoints  

### **GET all KSBs**  
- **Endpoint:** `GET /ksbs`  
- **Response:** `200 OK` (returns a list of all KSBs)  

### **GET all knowledge KSBs**  
- **Endpoint:** `GET /ksbs/knowledge`  
- **Response:** `200 OK` (returns a list of all knowledge KSBs)  

### **GET all skill KSBs**  
- **Endpoint:** `GET /ksbs/skill`  
- **Response:** `200 OK` (returns a list of all skill KSBs)  

### **GET all behaviour KSBs**  
- **Endpoint:** `GET /ksbs/behaviour`  
- **Response:** `200 OK` (returns a list of all behaviour KSBs)  

### **GET a specific KSB by UUID**  
- **Endpoint:** `GET /ksbs/{uuid}`  
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Response:** `200 OK` (returns the requested KSB)  

### **POST a new KSB**  
- **Endpoint:** `POST /ksbs/{type}` (`type` must be `knowledge`, `skill`, or `behaviour`)  
- **Payload:**  
  ```json
  {
    "code": 12,
    "description": "Automate tasks where it introduces improvements to the efficiency of business processes and reduces waste, considering the effort and cost of automation."
  }

### **DELETE a specific KSB by UUID** 
- **Endpoint:** `DELETE /ksbs/{uuid}`
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Response:** `204 NO CONTENT`

### ••UPDATE/PUT a ksb**
- **Endpoint:** `DELETE /ksbs/{uuid}`
- **Example:** `/ksbs/43300ad3-d6ef-4807-a35f-73752b47d897`  
- **Payload:** 
```json
{
  "type": "knowledge", 
  "code": 12
}
```
(`payload` can include `type` and/or `code` and/or `description` )