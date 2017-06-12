# this is for the photographer doing a mariage shoot
# and inviting clients to buy (proofing)

# this needs a new kind of authentication different from microstock selling
# the pictures need to be protected even the watermark should be hidden

# photographer could create an account onb behalh of the cleint 
# there could be a 2nd type of account
# but then besides transmitting uid, aid, you should also transmit cid
# (iid as invited id)
# 
# =====================
# invite to a gallery: email address + password
# then equivalent to 'insecret': isinvited
# they can view the watermarked
# this is a new permissions: sell to invitees: i

# one gallery may have several invitees
# like freinds

# solution:
# ===========
# each gallery has one invitesecret field
# if permission is set to 'i', then this field is used
# the field can be given in advance to a client, before the gallery is even created
# there are loose contraints on complexity (can be relatively short)
# but it is not enough to view the gallery
# you need also to have an email address (conatins a @) or username
# in the list of gallery's invites
# user/1/gallery/22/invite/333
# invite={id,email)
# can send mail: go to /user/1/gallery/22
# and user username: the_email, password: the invite key
# if password and secret match, then set a session cookie
# (and HTTP Basic?) could be done in theroy
# but has to make the difference between authenticated and authinvited
# iid
# can merge a atpic account with iid
# there is a search
# alex.atpic.com/find
# username:
# key: 
# (this is different from login)
# if authenticated, then check the list of invitess
# and lists the gallery the atpic user is allowed to see
# if the is exactly one gallery with that email and secret, then display it
# there may be more than one
# should we inforce unicity on (user,secret)???

# once invauthenticated, store the session in a new crypted cookie (user,secret)
# same as secret key: do we store it in a new cookie?


# the BIG difference here is that you do not need to know the gallery ID to invite
# you can invite in ADVANCE! without knowing the galleary ID
# this a bit similar to having a /tree path, but it can be then hidden
# and knowing onbly the path is not enough: you need a pair (email,secret)


# ===============================
# a photographer takes a session of pictures (wedding)
# he gives an invite ID, e.g sending to the customer email address a secret
# and his web site address:
# pdns.faa/show
# when he gets home he goes to that gallery, and make it vieweable
# with email+secret
# atpic searches the galleries with that secret (restrict to that account?)

# ================================
# for each gallery, then is a secret field
# and a invite email
# then to find we do a search with invite email + invite key
# we send a cookie invite_123 ( gallery ID)
# same thing for private with key
# then a invited can log into his account and add this gallery
# (the gallery has a list of 'friend' not really a friend but similar
