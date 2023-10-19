# you need to be totally rock solid in these areas so lets re-cap
# this lesson is boring and you prolly know most of it but i can't build on shaky foundations
# i tend to call lists[] an array and dicts{} an object, but they are both arrays as are tuples and sets
# we will have nested arrays, arrays of objects and objects containing arrays and can get complicated
# you have to be clear on how they bolt together and the when, where and why to use the right type
# we will eventually use several languages so i will often use different words for the same thing

# go to end of file and uncomment a section to run it

# After this re-cap you should be able to visualise in your mind a deep nest of arrays and 
# how to iterate them and get and set the values stored in them


# First python lines: always import any libraries or packages we might need first
import time

# declare or initialise any global variables we will be using
# globally declared variables means we can access them in any function without passing them in

messages = ['msg A', 'msg B', 'msg C'] # a simple list[] array with keys or indexes 0,1,2 automatically assigned
messages_sent = [] # an empty array we can append into

# you access a simple list[] element using it's numerical key 
# get the value: messages[1], set the value messages[1] = 'blah'
# NB you always need the numerical key to get or set the row or element value



# after globals we define all our functions, no stray code in here just functions!
# functions have to exist BEFORE they are called or used
# NB: the very last function will be called main(), it can be anything but main is common.


def variables():
    # a variable can be a: 
    # string, number, boolean (True/False), date object, array or list etc
    # if you print the variable name it actually prints the value or content of the variable
    myname = 'bob smith'
    print('myname = ', myname)
    print('len = ', len(myname)) # len() of a string gives the number of charactors

    # if you make a copy of myname and change one it doesn't change the other
    myname2 = myname # copy the original, both now have the value of  bob smith
    myname2 = 'fred jones' # change the value of the cloned item
    print('myname = {} myname2 = {}'.format(myname, myname2)) 
    # it doesn't change the orignal
    # if you copy an array: new_messages = messages they are the very same thing, change one you change both
 
def listArrays():
    # arrays are variables that have multiple values neatly tucked inside
    # simple arrays list[] are often called key value pairs, you need the numerical key or index to get the value
    # to get a value from a simple list[] array you NEED it's key aka row number or index or position
    print('messages[0] = ', messages[0])
    print() # just prints an empty line 

    # append or add a new item to the end of the list
    messages.append('msg D')
    print()

    # we can get the numer of items in an array using len()
    # len(messages)-1 will give us the last row index
    print('messages count = {} last index = {}'.format(len(messages), len(messages)-1))
    print()
    last_message_index = len(messages)-1
    print('First message = {} Last message = {}'.format(messages[0], messages[last_message_index]))
    # NB: messages[6] does not exist and will throw an error if you try to call it

    # another way to get the first and last is by getting zeroeth item, 
    # then reverse the array and get the zeroeth item
    messages.reverse()
    print('Reversed: last now the zeroreth = ',messages[0])
    messages.reverse() # put the array back
    # this is handy because the zeroeth item nearly always exists and not throw an error!
    print()

    # you can delete and update etc but you need the key or row number
    # without a key you can't even get the value or content
    # if you know the value you can get the key, it will return the very first match it finds, beware duplicates
    print('position or index of "msg C" = ', messages.index('msg C'))
    # you can delete array items but the keys will change - beware
    # you can put arrays inside array values (nested) but we wont cover that today if ever

    # in the original messages app you copied whole the message into the sent list
    # if the message was very long we soon have a huge list
    # if we send that message to 100 users we have hundreds of copies of long text
    # we could just store the message key in the sent list which would point back to the original message
    # important you get this bit, it's called normalizing your code, no duplicates if possible

    # lets say we want to store message[1] and 2 in the sent list 
    messages_sent.append(1)
    messages_sent.append(2)
    print('All the sent messages values', messages_sent)
    # sent has the key the messages list, we can use that to print the orginal message

    print('The zeroeth message sent', messages[messages_sent[0]])# the zeroeth message_sent has the value 1
    # its the same as saying print(messages[1])
    # this way we only keep numbers in sent not huge swathes of duplicate text

    # lets iterate or walk through the sent_messages and print out the original message
    # there are several ways to do this. We can call each item msgKey or x or whatever we want during the loop
    
    for msgKey in messages_sent:
        print(msgKey, messages[msgKey])
    
    print()
    # as long as the original message doesn't change this method will work fine

    # if we needed the sent_message index or key as well as it's value during the loop we need another method of walking
    # one way is to use the range(), range(5) will get 5 items, if we use the highest key from len() it will do them all
    for i in range(len(messages_sent)):
        print('Loop {} messages_sent index = {} sent_message value = {} message[{}] = {} '.format(i, i, messages_sent[i], i, messages[messages_sent[i]])) # prints the index of the sent message
    
    
    messages_sent.clear() # reset the sent items list
    print()

    # nested arrays, 
    # thinking of a user each row has a name,email,phone address etc
    user = ['bob', 'smith', ['19 london road','nottingham', 'ng1 3ll']]
    # last item is an array with 3 elements or values
    # user[0] is the first name, user[1] is the last name
    # user[2] is an array so to get the postcode it woulld be
    # postcode = user[2][2] this works but isn't very friendly and deeper nests gets worse
    print('user array = ', user)
    print('postcode = ', user[2][2]) # it's ok as long as you know what all the numbers mean!
    print()

    # back to the task in hand, two functions, one to send and one to print sent
    # in your original app it simply iterated the messages (and sends the mail?)  and puts a copy in the sent list
    def send_all():
        for i in range(len(messages)):
            # insert code to send message here <--
            messages_sent.append(i)

    # we also needed to print a list of sent messages
    def print_sent():
        messages_sent.reverse()
        for msgKey in messages_sent:
            print('sent ', messages[msgKey])

    send_all()
    print_sent()

    # so thats it, all done in a few lines of easy to follow clean code

    # main problem is that it sends all the messages to all the users all the time
    # in reality we will have a single message that goes out to a list of users
    # the print list is also useless, doesn't tell us what date or who sent it to who and whether it failed 
    # what happens when the list is too long?
    # right now we are clearly missing a list of users with contact details
    # the users may have a preferred method of contact, email, mqqt, phone, telegram
    # These are all things to be addressed next and simple indexed arrays won't cut the mustard

    # PS: did you notice i created two functions send_all() and print_sent() INSIDE the simpleListArrays() function?
    # you can tell me what you think about that we next meet!

def dictLists():
    print('Working with dict{} objects')
    # dict{} or objects are way more easy to use, we use a name rather than an  index number to access it
    # consider the user details we will need in the previous
    andy = {'first_name': 'andy', 'last_name': 'Mac', 'email': 'aMac@b', 'phone': '+44 (0) 77777 66666'}
    print(andy)
    print('email = ', andy['email']) # very easy to follow this code
    print()
    # what if the user had an address with several parts in it
    # we can add a new property or name or field like this
    # we are making the content of a dict property a dict{}, eg; a dict inside a dict
    andy['address'] = {'street': '98 Lampard Ave', 'city': 'Nottingham', 'postcode': 'NG2 6ZZ'}

    print(andy)
    print('postcode = ', andy['address']['postcode'])
    print()
    # we will eventually do this for both the messages and sent because they will both 
    # need these friendly field names instead of numbers

    # we will have multiple users, so we store each use object in simple array so we can loop them
    users = [] # declare an empty array
    users.append(andy)

    # create another user in one long string
    andyM = {'first_name': 'andy', 'last_name': 'Maddock', 'email': 'a@Maddock', 'phone': '+44 (0) 77777 232323', 'address': {'street': '98 Hackers Ave', 'city': 'Nottingham', 'postcode': 'NG24 6QQ'}}
    users.append(andyM)

    # we now have 2 users in a simple array  users[0] and users[1] 
    # we already know how to iterate a simple list each elemnt at a time and access any property
    # we can add new property's at any time, lets add a preferred contact method to each user
    # the row number isn't much use, users will have a corp ID number too
    users[0]['contact_method'] = 'email'
    users[0]['id'] =  1234
    users[1]['contact_method'] = 'mqtt'
    users[1]['id'] = 5678


    print('user[0] contact method] = ', users[0]['contact_method'])
    print('user[1] contact method = ', users[1]['contact_method'])
    print()

    # below is a neat way of iterating and finding stuff using the next function 
    # find a user with id = 1234 then try with an non existant id 8778777
    # i'm not gonna explain how this works this right now, you just need to know it can be done
    user = next((item for item in users if item["id"] == 5678), False) # will return False if not found
    if(user):
        print('user email = ', user['email'], ' user id = ', user['id'])
    else:
        print('user not found')

    # we might just want the users array index or row number not the whole user object
    row_number = next((i for i, user in enumerate(users) if user["id"] == 5678), False)
    print('user id = 5678 has row number = ', row_number)

    # what if there are mulitple results, search for andy?
    # this method only gets the first match but there are two
    user = next((item for item in users if item["first_name"] == 'andy'), False) 
    print('first matching user for andy = ', user['email']) # returns just the first one it found
    print()

    # we can use the list and filter methods and return an array list[] of matching rows
    user = list(filter(lambda person: person['first_name'] == 'andy', users))
    print('found {} rows with first_name = andy'.format(len(user)))
    print('user[1][email] =', user[1]['email'])

    # what we learnt here is 
    # dict{} contain multiple fields and are easy to read
    # they are often kept in simple list[] arrays
    # they can be sorted and filtered with various search methods
    # not to rely on the row number or index key of a simple array because if one is removed keys will change

    # to send out a message to a list of users all we need is a of list their id numbers
    # we can look up each users properties using the id as we loop the list avoiding duplication
    # security, if the list of user id's gets accidentally sent out it would be meaningless and has no details




# Main() always runs, it calls all the other functions
# uncomment a single line at a time so the output isn't cluttered when you run the script
def main():
    print('Main function called\n')
    variables()
    #listArrays()
    #dictLists()
    # that's it, we will use everything in here at some stage
    # from here on it's a doddle
    # in the next step we will build a running basic version in just a few lines of code hopefully


# just run main() to kick the entire app off
# its always the next line after the main function
main()

