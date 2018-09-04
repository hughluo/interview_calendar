### Usage
`
GET localhost:5000/api/candidates/<int:cid>/matching
`

### Description

Get a collection of matching slots with interviewer(s) for a candidate.

### Parameters

<int:cid> is the id of candidate you want to get matching for.

Use query to transfer the array that contains ids of interviewers you want to match up with given candidate via a key-value pair.

* iids: an array contains id(s) of interviewer(s)

One thing you should pay attention to is that even if there is only one interviewer you want to match up with, you should still use an array to contain its id.

## Response

A array contains slots.

A single slot is a dict look like this:

```
m = {
    't_start': <int: slot start epoch time>,
    't_end': <int: slot end epoch time>,
    'cid': <int: id of candidate>,
    'iids': <array: list contains ids of interviewer>,
}
```

## Errors

#### 400 Bad request
1. **Candidate not exists**

    No candidate with given id could be found.

2. **Iids is illegal**

    The iids is invalid or it contains id by which no interviewer could be found.

## Example


Let's say we have a candidate with cid 1 and
three interviewers with iid 1, 2 and 3 separately.
And a single interview last one hour. All interviews should begin sharp and end sharp.

Here is the slots we already set:

| Candidate id | Slot |
| ----------- | ----------- |
| 1 | 2018/9/9 9:00 ~ 2018/9/9 12:00|

| Interviewer id | Slot |
| ----------- | ----------- |
| 1 | 2018/9/9 9:00 ~ 2018/9/9 10:00|
| 2 | 2018/9/9 9:00 ~ 2018/9/9 11:00|
| 3 | 2018/9/9 10:00 ~ 2018/9/9 12:00|

So we can get the following matching result:

| Slot | Candidate id | Interviewer id |
| ----------- | ----------- | ----------- |
| 2018/9/9 9:00 ~ 2018/9/9 10:00| 1 | 1, 2 |
| 2018/9/9 10:00 ~ 2018/9/9 11:00| 1 | 2, 3 |
| 2018/9/9 11:00 ~ 2018/9/9 12:00| 1 | 3 |

In this document we will not discuss how to add slots, if you want to learn more about that, please check add_slot.md instead.

Only the matching is what we interested in here.

Following url is the request to query for matching slots with the three interviewers (whose iid is 1, 2 and 3 separately) for candidate whose cid is 1 :


`
localhost:5000/api/candidates/1/matching?iids=[1, 2, 3]
`  

And here is the response should looks like:

```
[
    {'t_start': 1536483600, 't_end': 1536487200, 'cid': 1, 'iids': [1, 2]},
    {'t_start': 1536487200, 't_end': 1536490800, 'cid': 1, 'iids': [2, 3]},
    {'t_start': 1536490800, 't_end': 1536494400, 'cid': 1, 'iids': [3]}
]
```


Please refer to the **matching test2** of **test_matching** in **test.py** for more details.
