import hashlib, chain, cPickle, random, string, time, reductor, conversions, cPickle, csv, sys, math

'''Some metrics based on different reductions schemes'''
# chri's -> 11/20
# inv st -> 13/20
# inv nd -> 7/20
# inv both -> 8/20

NUM_CHARS = 0
NUM_CHAINS = 0
CHAIN_LEN = 0

def get_table(num_chars, num_chains, chain_len, debug=False):
	# We check to see if a table has already been generated
	try:
		return get_old_table()
	except:
		print 'No pre-generated tables were found...'
		print 'Generating chains...'

	# We save to a file for faster table generation
	# Table too big to be kept in memory
	f = open('rbtb.txt', 'wt')
	writer = csv.writer(f)

	for x in range(num_chains):
		if x % 1000 == 0:
			print 'have generated %i chains' % (x)

		rnd_string = ''.join(random.choice(string.lowercase) for i in range(num_chars))
		(chain_head, chain_end) = chain.create_chain(rnd_string, chain_len, debug)

		writer.writerow((chain_head,chain_end))

	print 'finished generating table...'

	return get_old_table()

# Loads previously generated table
def get_old_table(tab_name='rbtb.txt'):
	table = {}
	with open(tab_name, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			table[row[0]] = row[1]
	return table

# Main function
def crackSHA1(hashval, num_chars, debug=False):
	global NUM_CHAINS
	global CHAIN_LEN
	global NUM_CHARS

	NUM_CHAINS=int(math.ceil((26**num_chars)**(2.0/3))*1.5)
	# NUM_CHAINS=75000

	CHAIN_LEN=int(math.ceil((26**num_chars)**(1.0/3))*1.5)
	# CHAIN_LEN=250

	NUM_CHARS=num_chars

	table = get_table(NUM_CHARS, NUM_CHAINS, CHAIN_LEN)
	
	list_hash = chain.get_list_red(hashval, NUM_CHARS, CHAIN_LEN)

	for (chain_head, chain_end) in table.iteritems():
		if chain_end in list_hash:
			res = chain.find_hash_in_chain(chain_head, hashval, CHAIN_LEN)
			if res != None:
				print 'We were able to recover this value => %s' % res
				return


	print 'The original value could not be recovered\n Try deleting your table and reruning'

if __name__ == "__main__":
	if len(sys.argv) == 3:
		print 'Attempting to recover...'
		print 'setting verbose mode off'
		crackSHA1(sys.argv[1], int(sys.argv[2]))
	else:
		print 'Attempting to recover...'
		print 'setting verbose val %s' % (sys.argv[3])
		crackSHA1(sys.argv[1], int(sys.argv[2]), bool(sys.argv[3]))