# Get
    This is a function that fetches data from the given DB connection mentioned in conf/SQL.properties file

### Syntax

```
get selection|tablename
```
Arguments,

1. `selection` : The list of columns that you want to select.
    
    Valid selections:
    - `all` or `*` to select all the columns
    - Valid column available in the conected DB 
2. `tablename` : The name of the table that you want to perform the selection.

## Example:

```
get *|Order
get all|order
get ID,OrderDate,OrderNumber|Order
```

