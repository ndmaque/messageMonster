# Basics: Lists[] and Dicts{} 
# They are the core of most apps and you need to be 100% rock solid before we start, the rest we can skim
# its a fasttrack situ right?

# you prolly know most of it but lets be sure
# you have to be clear on how they bolt together and the when, where and why to use the right type
# we will look at nested arrays, arrays of objects and objects containing arrays

# i tend to:
# use single quotes, why use double anything? i'm lazy, no shift key required
# call lists[] a simple or indexed or keyed array 
# call dicts{} an object, but they are both arrays as are tuples and sets
# use .format() to put variables into strings

# NB: Go to end of this file and uncomment a section in main() 

# After this re-cap you should be able to visualise in your mind a deep nest of [] and {} and 
# how to iterate them and get and set their values or content
# we can move very fast once i know you have this solid understanding

# =============================================================

# START
#
# declare or initialise any global variables here at the top jst after any imports
# globally declared variables means we can access them in any function without passing them in

# create a simple list[] array with 3 values, the keys or indexes 0,1,2 are automatically assigned
messages = ['msg A NAS 1234 down', 'msg B lost connection to HQ', 'msg C']

# an empty array that we can populate later
messages_sent = [] 

# you access a simple list[] element using it's numerical key 
# get the value: messages[1] 
# set the value: messages[1] = 'blah'
# NB: you usually need the numerical key to get or set a simple list[] array value


# after our global variables we define all our functions
# no stray code in here just pure functions!
# functions have to exist BEFORE they are called
# NB: the very last function shalst be called main(), it will make sense later

def variables():
    # a variable can be a: 
    # string, number, boolean, date, array or list etc
    # a variable with a string value is as simple as it gets

    myname_1 = 'bob smith'
    print('myname1 = ', myname_1)
    print('length = ', len(myname_1)) # len() of a string gives the number of charactors
    print()

    myname_2 = myname_1 # create a new variable with the value of myname_1, both have the value of  bob smith
    myname_2 = 'fred jones' # now change the value of myname_2
    print('myname_1 = ', myname_1)
    print('myname_2 =', myname_2) 

    # changing the value in myname_2 didn't change the value of myname_1
    # whereas if you copy an array: new_messages = messages they become the very same thing
    # change a value in one array and you ALL copies
 
def listArrays():
    
    # arrays are variables that have multiple values neatly tucked inside
    # list[] arrays aka simple or index or keyed arrays are often called key value pairs, you need the numerical key or index to get the value
    # to get a value from a simple list[] array you NEED it's key aka row number or index or position
    print('messages[0] = ', messages[0])
    print() # this just prints an empty line as a seperator

    # append or insert a new item to the end of the list
    messages.append('msg D')

    # we can get the number of rows or items in an array using len()
    # len(messages)-1 will give us the last row or index we can use
    print('messages count = {} last index = {}'.format(len(messages), len(messages)-1))
    print()

    last_message_index = len(messages)-1
    print('First message = {} Last message = {}'.format(messages[0], messages[last_message_index]))
    # NB: messages[6] does not exist and will throw an error if you try to call it

    # another way to get the first and last is by getting zeroeth item, 
    # then reverse the array and get the zeroeth item
    messages.reverse()
    print('Reversed: the last entry is now the zeroreth = ',messages[0])
    messages.reverse() # put the array back
    # this is handy because the zeroeth item nearly always exists and not throw an error!
    print()

    # if you know the value in an array you can get its key
    # array.index() it will return the very first match it finds
    print('index first message that = "msg C" = ', messages.index('msg C'))
    # you can delete array items but the keys will change so beware
    # you can put list[] arrays inside list[] array values (nested) but it can get messy

    # in your original knock up messages app you copied the whole message into the sent list
    # if each message was very long we soon have a huge list of duplicates
    # we could just store the message key in the sent list which would point back to the original message
    # important you get this bit, just store to row number into sent, no need for the whole message

    # lets say we want to put message[1] and message[2] in the messages_sent list
    messages_sent.clear()
    messages_sent.append(1) # the second message B
    messages_sent.append(2) # the third message C

    # lets iterate or walk through the messages_sent values and print out the original message
    # there are several ways to do this. 
    # NB: we can call each item val or x or whatever we want during the loop, we'll use val in this example
    
    for val in messages_sent:
        print(val, messages[val])
    
    print()

    # as long as the original message doesn't change this method will work fine

    # if we needed the messages_sent index or key as well as it's value during the loop we need another method of walking
    # one way is to use the range(), range(5) will get 5 items
    # if we use the highest key from len() it will do them all
    # we often use i in in this situ because it's a numerical increment counter
    for i in range(len(messages_sent)):
        print('i = {} messages_sent[{}] = {} message[{}] = {} '.format(i, i, messages_sent[i], messages_sent[i], messages[messages_sent[i]])) # prints the index of the sent message
    
    # we can reset or empty the messages_sent list
    messages_sent.clear() 
    print()

    # nested arrays
    # example of a user profile, each user has a name,email,phone address etc, the address has multiple parts, city zip etc
    # below the value in user[2] is the address array
    user = ['bob', 'smith', ['19 london road','nottingham','ng1 3ll']]
    # user[0] is the first name, user[1] is the last name
    # user[2] is an array so to get the postcode it would be
    # postcode = user[2][2] works but isn't very friendly
    print('user nested array = ', user)
    print('postcode for user[2][2] = ', user[2][2]) # it's ok as long as you know what all the numbers mean!
    print()

    # back to the task in hand, your original code yoy looped the messages and put content into sent and then printed the sent right?
    # i see two functions needed, one to loop and send, and one to print the sent
    def send_all():
        # we use the range method, it means the i is the row number not the actual value like before
        for i in range(len(messages)):
            # TODO insert some code here to actually send the message
            # if you needed the value of this message you use message[i] but we only need its row number aka key/index
            messages_sent.append(i)

    # we also need a method to print a list of sent messages
    def print_sent():
        messages_sent.reverse() # reverse the list so it's Last In First Out aka LIFO
        for val in messages_sent:
            print('Reversed messages_sent[{}] ] {}'. format(val,messages[val]))
        
        messages_sent.reverse() # put the list back!

    send_all()
    print_sent()

    # so thats it, all done in 2 functions and 6 lines of easy to follow code

def dictLists():
    print('Working with dict{} objects')
    messages_sent.clear()

    # dict{} or objects are way more easy to use, we use a name rather than an  index number to access it
    # consider the user details we will inevitably need
    user = {'first_name': 'andy', 'last_name': 'Mac', 'email': 'aMac@b', 'phone': '+44 (0) 77777 66666'}
    print('user[email] = ', user['email']) # very easy to follow this code
    print()

    # what if the user object also had an address part with several lines in it
    # we can add a new property or name or field to the user like this
    # we are making the content of a dict property a dict{}, eg; a dict nested inside a dict
    user['address'] = {'street': '98 Lampard Ave', 'city': 'Nottingham', 'postcode': 'NG2 6ZZ'}

    print(user)
    print('postcode = ', user['address']['postcode']) # the code makes sense unlike user[0][2]
    print()

    # we will have multiple users, so we store each user dict into a simple array
    users = []
    users.append(user)

    # create another user 
    user = {'first_name': 'andy', 'last_name': 'Maddock', 'email': 'a@Maddock', 'phone': '+44 (0) 77777 232323', 'address': {'street': '98 Hackers Ave', 'city': 'Nottingham', 'postcode': 'NG24 6QQ'}}
    users.append(user)

    # we now have 2 users in a simple array  users[0] and users[1] 
    # we can add new property's at any time, lets add a preferred contact method to each user
    users[0]['contact_method'] = 'email'
    users[1]['contact_method'] = 'mqtt'
    # and a corporate unique user id or name because we can't rely on the row number is a unique identifier
    users[0]['id'] = 1234    
    users[1]['id'] = 5678
    
    print('user[0][contact_method] = ', users[0]['contact_method'])
    print('user[1][contact_method] = ', users[1]['contact_method'])
    print('user[1][address][city] = ', users[1]['address']['city'])
    print()

    # Searching and filtering
    # below is a neat way of finding rows using the next function 
    # find a user with id = 5678 then try with an non existant id 8778777
    # i'm not gonna explain how the next line works right now, you just need to know it can be done

    user = next((item for item in users if item['id'] == 5678), False) # will return False if not found
    if(user):
        print('Search found user id = {} email = {}'.format(user['id'], user['email']))
    else:
        print('No user found')

    # we might just want the index or row number of the users array and not the whole user object
    index = next((i for i, user in enumerate(users) if user['id'] == 5678), False)
    print('user id = 5678 is in row number = ', index)

    # what if there are multiple results? search for 'andy'
    # this method only gets the first match to 'andy' but there are two
    user = next((item for item in users if item['first_name'] == 'andy'), False) 
    print('first found matching user for andy = ', user['email']) 
    print()

    # this method finds all matches and puts them in a simple list array
    results = list(filter(lambda person: person['first_name'] == 'andy', users))
    print('found {} rows where first_name = "andy"'.format(len(results)))
    print('user[1][email] =', results[1]['email'])

    # what we learnt here is 
    # dict{} contains multiple properties or fields and are easy to read
    # users[2][3][1] sucks!    
    # dicts{} are often kept inside simple list[] arrays
    # both can be sorted and filtered with various search methods
    # never rely on the row number or index key of a simple array because if one is deleted they keys will change
    # try not to copy or duplicate stuff but point to the original source where possible





# always have function called main() as the last function which calls all the other functions
# uncomment a single line at a time below so the output isn't cluttered when you run the script
def main():
    print('Main function called\n')
    #variables()
    #listArrays()
    #dictLists()

# just run main() to kick the entire app off
main()


    # main problem is that it sends all the messages to all the users all the time
    # in reality we will have a single message that goes out to selected users or groups
    # the messages_sent list is useless, doesn't tell us what date or who sent it to who and whether it failed 
    # what happens when the list gets crazy long?
    # the messages_sent list is empty every time you run the script
    
    # Those are a few of the things to be addressed as we build the app
 