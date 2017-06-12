from twisted.cred import portal
from twisted.protocols import imap4

class Account:
    __implements__ = (imap4.IAccount,)
    
# Actually implement the interface here
    
    
def logout():
    # Cleanup logic goes here
    pass

class Realm:
    __implements__ = (portal.IRealm,)
    
def requestAvatar(self, avatarID, mind, *interfaces):
    if imap4.IAccount not in interfaces:
        raise NotImplementedError
    return imap4.IAccount, Account(avatarID), logout

p = portal.Portal(Realm())

# Contrive to have your ServerFactory's buildProtocol
# set the "portal" attribute of the IMAP4Server instance
# it creates to the `p' defined above.

