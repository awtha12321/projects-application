-- Keep a log of any SQL queries you execute as you solve the mystery.
------I used DB browser to make this project------

--* *find name by using phone number that i marked

--checking about crime to get description

SELECT description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

--checking the interviews

SELECT name, transcript
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;


--checking the exit between 15 min and 25
--cuz the interview said within ten minutes

SELECT activity, license_plate
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 and 25
ORDER BY license_plate ASC;

/*
exit	0NTHK55
exit	322W7JE
exit	4328GD8
exit	5P2BI95
exit	6P58WS2
exit	94KL13X
exit	G412CB7
exit	L93JTIZ
*/

--checked the Fifer street to get name, atm_transactions.account_number, transaction_type
--and i compared them with the result which i got from the above one


SELECT name, atm_transactions.account_number, transaction_type, atm_location
FROM bank_accounts
INNER JOIN people ON bank_accounts.person_id = people.id
INNER JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = 'withdraw';

/*
Luca	28500762	withdraw	Leggett Street --

Bruce	49610011	withdraw	Leggett Street
Alan	47306903	withdraw	Daboin Sanchez Drive
Jennifer	55656186	withdraw	Carvalho Road
Harold	65190958	withdraw	Humphrey Lane
Christian	45468795	withdraw	Carvalho Road
Samantha	70992522	withdraw	Daboin Sanchez Drive
Keith	14180174	withdraw	Carvalho Road
Theresa	46222318	withdraw	Humphrey Lane
Lisa	34939061	withdraw	Humphrey Lane
Anna	55322348	withdraw	Humphrey Lane
Amanda	90209473	withdraw	Humphrey Lane
Diana	26013199	withdraw	Leggett Street
Rachel	93903397	withdraw	Humphrey Lane
Douglas	57022441	withdraw	Daboin Sanchez Drive
Douglas	57022441	withdraw	Humphrey Lane
Ryan	76849114	withdraw	Humphrey Lane
Paul	50380485	withdraw	Humphrey Lane
Nicholas	97338436	withdraw	Carvalho Road
Jesse	26191313	withdraw	Daboin Sanchez Drive
Rose	19531272	withdraw	Blumberg Boulevard
Laura	89843009	withdraw	Humphrey Lane
Brooke	16153065	withdraw	Leggett Street
Jack	69638157	withdraw	Humphrey Lane
Ernest	58673910	withdraw	Humphrey Lane
Denise	58552019	withdraw	Humphrey Lane
Sean	66254725	withdraw	Carvalho Road
Rebecca	92647903	withdraw	Humphrey Lane
Rebecca	92647903	withdraw	Humphrey Lane
Carol	20774848	withdraw	Daboin Sanchez Drive
Olivia	99835463	withdraw	Daboin Sanchez Drive
Christine	15452229	withdraw	Blumberg Boulevard
Joshua	69278040	withdraw	Carvalho Road
Joe	66454844	withdraw	Carvalho Road
Kenny	28296815	withdraw	Leggett Street
Margaret	74812642	withdraw	Blumberg Boulevard
Iman	25506511	withdraw	Leggett Street
Luca	28500762	withdraw	Leggett Street
Carina	75571594	withdraw	Blumberg Boulevard
Mark	17171330	withdraw	Blumberg Boulevard
Donna	41935128	withdraw	Humphrey Lane
Sharon	57029719	withdraw	Carvalho Road
Arthur	92206742	withdraw	Blumberg Boulevard
Dennis	21656307	withdraw	Daboin Sanchez Drive
Taylor	76054385	withdraw	Leggett Street
Julia	87859883	withdraw	Daboin Sanchez Drive
Michelle	79165736	withdraw	Humphrey Lane
Alexis	95773068	withdraw	Humphrey Lane
Joan	99031604	withdraw	Humphrey Lane
Shirley	67735369	withdraw	Daboin Sanchez Drive
Charles	40665580	withdraw	Daboin Sanchez Drive
Charles	40665580	withdraw	Humphrey Lane
Albert	40231842	withdraw	Carvalho Road
Christina	96336648	withdraw	Humphrey Lane
Jeremy	16113845	withdraw	Daboin Sanchez Drive
Pamela	16654966	withdraw	Daboin Sanchez Drive
Andrea	26797365	withdraw	Humphrey Lane
Stephen	13156006	withdraw	Humphrey Lane
Hannah	62690806	withdraw	Carvalho Road
Andrew	79127781	withdraw	Humphrey Lane
Janet	93401152	withdraw	Daboin Sanchez Drive
Benista	81061156	withdraw	Leggett Street
Zachary	66344537	withdraw	Humphrey Lane
Zachary	66344537	withdraw	Humphrey Lane
Ethan	97773635	withdraw	Carvalho Road
David	59116006	withdraw	Carvalho Road
*/

--checking everyone who has talked less than a min
--and after I get the thief, i will also know the ACCOMPLICE

SELECT caller, receiver, duration
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 And duration BETWEEN 0 AND 60
ORDER BY duration ASC;

/*
(499) 555-9472	(892) 555-8872	36 -
(031) 555-6622	(910) 555-3251	38
(286) 555-6063	(676) 555-6554	43 -
(367) 555-5533	(375) 555-8161	45 - Bruce	5773159633  Robin	NULL
(770) 555-1861	(725) 555-3243	49
(499) 555-9472	(717) 555-1342	50
(130) 555-0289	(996) 555-8899	51 - Sofia	1695452385 -- Jack	9029462229
(338) 555-6650	(704) 555-2131	54
(826) 555-1652	(066) 555-9701	55 -- wrong
(609) 555-5876	(389) 555-5198	60
*/

--i got the phone numbers from the above one
--so i can use phone numbers to get passport_numbers and names

SELECT name, passport_number
FROM people
WHERE phone_number = '(389) 555-5198';

/*
Luca	8496433585
Kathryn	6121106406
Kenny	9878712108
Doris	7214083635
Sofia	1695452385
Bruce	5773159633
Robin	NULL

*/

-- i did this to get the excat hour and minute for the next code
--the day is 29 cuz the interview said so

SELECT origin_airport_id, destination_airport_id, hour, minute
FROM flights
WHERE year = 2021 AND month = 7 AND day = 29
ORDER BY origin_airport_id ASC;

--i got the theif by comparing his passport_number in the pessengers

SELECT passport_number, origin_airport_id, destination_airport_id
FROM passengers
INNER JOIN flights ON passengers.flight_id = flights.id
WHERE year = 2021 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20;

/*
7214083635	8	4   Doris	7214083635	(066) 555-9701 --
1695452385	8	4   Sofia	1695452385	(130) 555-0289 --
5773159633	8	4   Bruce	5773159633	(367) 555-5533 --
1540955065	8	4   Edward	1540955065	(328) 555-1152
8294398571	8	4   Kelsey	8294398571	(499) 555-9472 -
1988161715	8	4   Taylor	1988161715	(286) 555-6063 -
9878712108	8	4   Kenny	9878712108	(826) 555-1652 --
8496433585	8	4   Luca
*/

--i got destination_airport_id from the above one
--so i used destination_airport_id to know where the thief escaped to

SELECT abbreviation, full_name, city
FROM airports
WHERE id = 4;