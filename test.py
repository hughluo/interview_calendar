from datetime import datetime
from utils import datetime2epoch, epoch2datetime
import unittest
from pymongo import MongoClient
from app.models.interviewer import Interviewer
from app.models.candidate import Candidate
import requests
import json


def initialize4test():
    """
    Drop database and add candidates & interviewers for test purpose
    """
    client = MongoClient()
    client.drop_database('calender')
    Candidate.new(name='C1')
    Interviewer.new(name='I1')
    Interviewer.new(name='I2')
    Interviewer.new(name='I3')


# in this test case, we use requests to simulate api consume.
class TestClassMethod(unittest.TestCase):
    def test_add_slot_c(self):

        initialize4test()

        dt1 = datetime(2018, 8, 8, 8)
        dt2 = datetime(2018, 9, 9, 9)
        dt3 = datetime(2018, 9, 9, 10)
        dt4 = datetime(2018, 9, 9, 11)
        dt5 = datetime(2018, 9, 9, 12)
        dt8 = datetime(2019, 1, 1, 1)

        et1 = datetime2epoch(dt1)
        et2 = datetime2epoch(dt2)
        et3 = datetime2epoch(dt3)
        et4 = datetime2epoch(dt4)
        et5 = datetime2epoch(dt5)
        et8 = datetime2epoch(dt8)

        url = "http://localhost:5000/api/candidates/1/slots"

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            'Postman-Token': "2a52c3f1-a56b-42a2-a9f6-10453e745913"
        }

        querystring1 = {"t_from": et2, "t_to": et5}
        response1 = requests.request("POST", url, headers=headers, params=querystring1)

        r = [{"t_from": et2, "t_to": et5}]
        rs = json.dumps(r)
        rse = rs.encode('ascii')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.content, rse)

        # Illegal. t_from should less than t_to
        querystring2 = {"t_from": et3, "t_to": et2}
        response2 = requests.request("POST", url, headers=headers, params=querystring2)
        self.assertEqual(response2.status_code, 400)

        # Illegal. t_from and t_to should both bigger than 'now' in epoch time
        querystring3 = {"t_from": et1, "t_to": et2}
        response3 = requests.request("POST", url, headers=headers, params=querystring3)
        self.assertEqual(response3.status_code, 400)

        # Illegal. t_from and t_to should both smaller than '2 month later' in epoch time
        querystring4 = {"t_from": et1, "t_to": et8}
        response4 = requests.request("POST", url, headers=headers, params=querystring4)
        self.assertEqual(response4.status_code, 400)

    def test_add_slot_i(self):
        initialize4test()

        dt1 = datetime(2018, 8, 8, 8)
        dt2 = datetime(2018, 9, 9, 9)
        dt3 = datetime(2018, 9, 9, 10)
        dt4 = datetime(2018, 9, 9, 11)
        dt5 = datetime(2018, 9, 9, 12)
        dt8 = datetime(2019, 1, 1, 1)

        et1 = datetime2epoch(dt1)
        et2 = datetime2epoch(dt2)
        et3 = datetime2epoch(dt3)
        et4 = datetime2epoch(dt4)
        et5 = datetime2epoch(dt5)
        et8 = datetime2epoch(dt8)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            'Postman-Token': "2a52c3f1-a56b-42a2-a9f6-10453e745913"
        }

        url1 = "http://localhost:5000/api/interviewers/1/slots"
        querystring1 = {"t_from": et2, "t_to": et3}
        response1 = requests.request("POST", url1, headers=headers, params=querystring1)
        r1 = [{"t_from": et2, "t_to": et3}]
        rs1 = json.dumps(r1)
        rse1 = rs1.encode('ascii')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.content, rse1)

        url2 = "http://localhost:5000/api/interviewers/2/slots"
        querystring2 = {"t_from": et2, "t_to": et4}
        response2 = requests.request("POST", url2, headers=headers, params=querystring2)
        r2 = [{"t_from": et2, "t_to": et4}]
        rs2 = json.dumps(r2)
        rse2 = rs2.encode('ascii')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.content, rse2)

        url3 = "http://localhost:5000/api/interviewers/3/slots"
        querystring3 = {"t_from": et3, "t_to": et5}
        response3 = requests.request("POST", url3, headers=headers, params=querystring3)
        r3 = [{"t_from": et3, "t_to": et5}]
        rs3 = json.dumps(r3)
        rse3 = rs3.encode('ascii')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.content, rse3)

    def test_matching(self):

        initialize4test()

        dt1 = datetime(2018, 8, 8, 8)
        dt2 = datetime(2018, 9, 9, 9)
        dt3 = datetime(2018, 9, 9, 10)
        dt4 = datetime(2018, 9, 9, 11)
        dt5 = datetime(2018, 9, 9, 12)
        dt8 = datetime(2019, 1, 1, 1)

        et1 = datetime2epoch(dt1)
        et2 = datetime2epoch(dt2)
        et3 = datetime2epoch(dt3)
        et4 = datetime2epoch(dt4)
        et5 = datetime2epoch(dt5)
        et8 = datetime2epoch(dt8)

        Candidate.add_slot_by_id(1, et2, et5)
        Interviewer.add_slot_by_id(1, et2, et3)
        Interviewer.add_slot_by_id(2, et2, et4)
        Interviewer.add_slot_by_id(3, et3, et5)

        url1 = "http://localhost:5000/api/candidates/1/matching"
        querystring1 = {"iids":"[1]"}
        headers1 = {
            'Cache-Control': "no-cache",
            'Postman-Token': "fc7bc0ff-37d9-4175-a234-6111685758f4"
            }
        response1 = requests.request("GET", url1, headers=headers1, params=querystring1)
        m1_raw = response1.content.decode('ascii')
        m1 = json.loads(m1_raw)

        self.assertEqual(m1[0]['t_start'], et2)
        self.assertEqual(m1[0]['t_end'], et3)
        self.assertEqual(m1[0]['cid'], 1)
        self.assertEqual(m1[0]['iids'][0], 1)

        # matching test2

        url2 = "http://localhost:5000/api/candidates/1/matching"
        querystring2 = {"iids":"[1, 2, 3]"}
        headers2 = {
            'Cache-Control': "no-cache",
            'Postman-Token': "fc7bc0ff-37d9-4175-a234-6111685758f4"
            }
        response2 = requests.request("GET", url2, headers=headers2, params=querystring2)
        m2_raw = response2.content.decode('ascii')
        m2 = json.loads(m2_raw)

        self.assertEqual(m2[0]['t_start'], et2)
        self.assertEqual(m2[0]['t_end'], et3)
        self.assertEqual(m2[0]['iids'][0], 1)
        self.assertEqual(m2[0]['iids'][1], 2)
        self.assertEqual(m2[1]['t_start'], et3)
        self.assertEqual(m2[1]['t_end'], et4)
        self.assertEqual(m2[1]['iids'][0], 2)
        self.assertEqual(m2[1]['iids'][1], 3)
        self.assertEqual(m2[2]['t_start'], et4)
        self.assertEqual(m2[2]['t_end'], et5)
        self.assertEqual(m2[2]['iids'][0], 3)


if __name__ == '__main__':
    unittest.main()
