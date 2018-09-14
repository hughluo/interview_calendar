### Usage

`POST localhost:5000/api/interviewers/<int:iid>/slots
`

`POST localhost:5000/api/candidates/<int:cid>/slots
`

This is a doc about adding slots for interviewers,
but it also applies for adding slots for candidate with following url.

One thing you should pay attention to is that cid and iid do not conflict with each other(which means you could have a candidate with cid = 1 and also a interviewer with iid = 1, since they are stored in different collections in mongodb).

### Description

Set an available interview slot

### Parameters

<int:iid> is the id of interviewer you want to set slot for.

Use query to transfer the slot data, which have two key-value pairs:
* t_from: time from, a int type epoch time

* t_to: time to, a int type epoch time

However, there are some **rules** about the epoch time when setting the slots. It applies for **both t_from and t_to**. Violating of following rules will raise 404 Bad request with message "Slot is illegal".

* The epoch time should be sharp(which means it's always 8 o'clock or 9 o'clock etc. but can never be like 8:15 or 9:45).

* The slot should last more than one hour.

* It can't be a slot after more than two months.

## Response

An array contains all slots (after this setting) for given interviewer.

## Errors

#### 400 Bad request
1. **Interviewer not exists**

    No interviewer with given id could be found.

2. **Slot is illegal**

    Slot is invalid. Please refer to the rules above.

## Example

Following request shows how to add a interview slot from epoch time 1536483600 to epoch time 1536487200 for interviewer whose id is 1.

`
localhost:5000/api/interviewers/1/slots?t_from=1536483600&t_to=1536487200
`



Response should look like this if it's the first time slot setting:

`
[{"t_from": 1536483600, "t_to": 1536487200}]
`
