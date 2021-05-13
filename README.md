# DomaciUkolTietoNetwork

The application periodically check the availability of end points.

## Input File
The Script reads end point from input.json:
```json
{ 
    "ipAddress": ["1.1.1.1",  "255.255.255.255" ,"10.11.12.255"]
}
```

## Output File
The script writes information for each end points to folder ouput to file out.html
![Show of output](https://i.imgur.com/hDdN3FW.png)

`Internet connection requried`

## Docker instruction:

### Build:
```bash
docker-compose build 
```

### Run:
```bash
docker-compose up
```