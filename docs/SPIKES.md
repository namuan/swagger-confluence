### Setup Confluence in Docker

Start Confluence in Docker using the following image

```
docker run --detach --publish 8090:8090 cptactionhank/atlassian-confluence:latest
```
Get the Evaluation license key and use it for the trial setup

Then we have setup an Admin (admin) user with password (P4ssw0rd)

Create a new Space "API Documentation"

Then add some content on the page

Then we need to enable and get API Tokens to access Confluence

We also created a jenkins user with the same password as above

Here is the API Flow
##### Find Pet Store Documentation in Confluence
```
curl "http://docker-ip:8090/rest/api/content?title=Pet%20Store%20Documentation&spaceKey=AD&expand=history" \
     -H 'Accept: application/json' \
     -H 'Content-Type: application/json' \
     -H 'Cookie: JSESSIONID=177797EC7B1F98A286ADAEBCB9D92D4D' \
     -u 'jenkins:***** Hidden credentials *****'
```

##### To Read Content based on the ID that we found

* Data from previous call
```
curl "http://docker-ip:8090/rest/api/content/{results[0].id}?expand=body.storage,version,space" \
     -H 'Accept: application/json' \
     -H 'Content-Type: application/json' \
     -H 'Cookie: JSESSIONID=177797EC7B1F98A286ADAEBCB9D92D4D' \
     -u 'jenkins:***** Hidden credentials *****'
```

##### To Update Page Content

* We need to increment version that we retrieve from the last call

```
curl -X "PUT" "http://docker-ip:8090/rest/api/content/{results[0].id}?expand=body.storage" \
     -H 'Accept: application/json' \
     -H 'Content-Type: application/json' \
     -H 'Cookie: JSESSIONID=177797EC7B1F98A286ADAEBCB9D92D4D' \
     -u 'jenkins:***** Hidden credentials *****' \
     -d $'{
  "body": {
    "storage": {
      "value": "Updated page",
      "representation": "storage"
    }
  },
  "id": "{results[0].id}",
  "title": "{results[0].id}",
  "space": {
    "key": "{space.key}"
  },
  "type": "page",
  "version": {
    "number": {version.number + 1}
  }
}'
```