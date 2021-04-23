# apollo-space-mission
## Project Description
Given google event data and transactional data, identify whether users placed orders and whether those orders we're succesful.

## Project Structure
```
.
├── apollo_space_mission
│   ├── data
│   │   ├── ga-sessions
│   │   └── transaction-data
│   ├── sql_queries # Part 1 Answers
│   │   ├── 1.sql
│   │   ├── 2.sql
│   │   ├── 3.sql
│   │   └── 4.sql
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── fixtures.py
│   │   └── test_utils.py
│   ├── __init__.py
│   ├── main.py # main entrypoint
├── .gitattributes # for git lfs
├── .gitignore   
├── Dockerfile
├── Pipfile
├── Pipfile.lock
└── README.md
```
## How to run
```docker build -t apollo .```<br/>
```docker run --rm -it apollo bash```<br/>
```python apollo-space-mission/main.py -vid fullvisitorId```
 
 (example vid: 6548322090645166416)

####For Testing

Note that this may take some time because of the integration tests.

```python -m pytest apollo_space_mission/tests```


### Future Considerations
1) The python problem states "provide the same analysis but building an application that is able to answer the question given a specific “fullVisitorId”", however since a fullVisitorId isn't unique (i.e. a client could have changed address and ordered in one session, but not another). Therefore, I chose the session with the greatest amounts of hits which would have  a strong chance of including an order placement. A more intelligent approach could involve filtering by order_confirmation within the session custom dimension and selecting the first occurence per fullVisitorId.
2) In line with the comment above, reporting back all of the orders placed and whether each one was successfully delivered per fullVisitorId is another valid interpretation of the question and could provide interesting insights.
3) SQL is not my mother tongue, and thus reviewing this code with someone else could help provide some optimizations (i.e. calculating the lat and long in the same table rather than merging them)
4) Setting the longitude and longitude a confidence interval of +/- 0.00001 as it appears the difference between some geopoints are nuances in location tracking on the phone rather than voluntary changes from the user.
5) Create a fake dataset for testing and create more testing (saving PI in repo is bad) 