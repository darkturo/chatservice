# Chat Service WebApp
This chat service webapplication is a message system that offers a classic chat
service via a secure channel and all using just a regular web browser with
JavaScript support.


## Introduction
The idea of this project is to provide a design an implementation that of a
complete scalable web application which implements a simple messaging/chat
service. This is a perfect excuse to play around with Python, Flask, Docker,
JavaScript, and other technologies.

The current implementation is just a prototype for the time being and there is
some of work to be done to complete the project.

The purpose of this document is to compile the design ideas behind the current
implementation as well as the desired features for this messaging/chat system.


## Desired Features
The Chat Service system is a web application that provides a scalable and
secure chat/messaging service via HTTP.

*  Allow users to find and read about other users;
   The system should provide means to search and find any user among the
   registered users.

*  Allow users to send and receive messages to/from each other;
   The system should provide a way to interchange text messages between two
   users that are registered (logged-in) the service. 
   The communication between two users registered in the system is always encrypted.
   
*  Allow users to send messages in named groups;
   The system provides a way to create groups where messages can be interchanges
   between many users. Also the communication between all the users in a
   certain group should be encrypted by default. Chat groups can be open (in
   which case they won't use encryption), or secure, in which case the members
   should approve new users that wants to join in. 
 
*  Allow users to read all messages they have ever sent or received; - Allow users to send messages “off the record” to another user;
   The system should have store all the interchanged messages in a
   conversation, this data is available to the users in the conversation.
   Also, the system should be able to send messages that are not stored "off
   the record"  in the database, or that has a certain duration.

*  Allow the system to serve up to 2 million users simultaneously; - Allow users to send 2 messages per second with a delay of <1s;
   The architecture of the system, the components that conforms it, as well as
   the code should be high performant and scalable.

*  Maintain full functionality for 99.995% of the time.
   The system should be fault-tolerant and be available up to 99.995% of the time.


## System Architecture
In this exercise I have decided to use python and flask to implement the web
application. 
Flask is a microframework that can be customized via plugins. There are
hundredths of plugins that allows to build a web application as if it was a
Lego(TM). Applications in Flask can be organised using a classic MVC pattern as
many modern web framework. What I consider specially interesting about flask,
despite the ability to build a system with just the components the current
application needs, is that it provides a URL routing mechanism via the use of
simple decorators, this makes really straight forward to build RESTful
webservices as well as webapplications with readable URLs.  

Because of the requirements (desired features) of the system, (almost) all the
messages will be encrypted and stored in a database. Both the procedure used to
encrypt the messages and the type of database could rapidly become a bottleneck
for the service when handling load.

In order to overcome these possible issues, the system could be modularized in
interconnected subsystems, so that is possible to scale the system vertically if
needed. Also the system should use asynchronous mechanisms to write/retrieve data
from the database, as well as threads to handle multiple requests per process.

The database could be a problem, so it could be interesting to have this in
mind during the design of the system, so its 'easy' to replace databases in
case that is a problem. For the time being though, a regular relational
database server should be enough.

A look into a modular system that matches the proposal can be the following:
 

```ascii
                               |
                               |
   Flask Service       Flask Service Runnign Mysql      Relational DB
   +----------+      +---------------------------+     +----------------------+
   |          |      |  Python Flask API/Backend |     |
   | FronEnd  |------|    (async writes to DB)   |-----| MySQL Database
   | HTML5+JS |      |  (and writes/reads cache) |     |
   +----------+      +---------------------------+     +----------------------+
 HTML   |               |  [ messages cache ]
 Presentation           |      |
 +------+               |      | 
 |  Web Browser         |      | Internal NW
 | +------------+       |      |
 +-|    www     |-------+
   +------------+  AJAX/HTTP

```


The Fron-End module just contains a web application that has the logic to
render templates, menus, and forms according to the screen flow of the
messaging system.
It uses JavaScript to interchange messages and requests with the BackEnd
module/service. It can handle accept multiple simultaneous request using flask,
and it relies most of the interaction flow to the JavaScript client. 

The BackEnd, will provide an Resftul API that allows a lightweight integration
with the JavaScript client, but also opens the possibility of integrating this
service with other services or be used from different front-ends. 
This BackEnd module has a cache, so the service can offload reads to the database.
Also the service should write asynchronously when possible, as well as
implement diverse heuristics to cache reads.
The BackEnd module should be created with the idea of being able to
organise a set of BackEnd modules to load balance.

The Relational DB can be just a basic Linux service running MySQL/MariaDB. 

The proposed architecture could support multiple horizontal scaling as well as
replication in order to allow 99.995% availability of the system.

### Front-End
The front-end could have as in the prototype the following screens (check the
prototype to find out the interactions):

 * Landing page

 * Register user page

 * Login user page (with captcha)

 * DM (Direct Message) page with an integrated search form/dialogue?

 * Group Message page with an integrated search for group/channels

 * An about/page

 * Perhaps a newspage

All the screens will use a dynamic menu which will adapt depending on whether
the user is logged in or not.
Also the user can freely navigate through these screens using readable URLs. 

### Back-End API
The system should provide the following restful API. The API allows read
without authentication, but all writes require the application/actor using the
API to have special credentials. Perhaps this can be achieves with OAuth (needs
some investigation). 

List of resources:

 * user

 * group

 * chat

List of operations (note that the API will use a JSON + URL encoding to
exchange information):

 * GET /user
   By default it should return a list of users (associated in some way)
   It allows URL encoded queries to define a search according to certain
   attributes.

 * GET /user/<user_name>
   Retrieve the profile of the user <user_name> that contains all its
   non-sensible information. Among this information the user has associated a
   public key that should be used to sign/encrypt or negotiate for a symmetric key.

 * POST /user/<user_name>
   Updates certain fields of the user <user_name>.

 * PUT /user/<user_name>
   Creates the user <user_name>


 * GET /group
   Retrieves a list of chat groups, associated in some way. It allows for URL
   encoded parameters to refine the search.

 * GET /group/<group_id>
   Equivalent to /user/<user_name> but for groups. All groups have assigned a
   public/private key that is generated by the BackEn. When requesting this
   resource the JSON will return the public key among other information.

 * POST /group/<group_id>
   Updates certain fields of the group <group_id>.

 * PUT /group/<group_id>
   Creates the group <group_id>.


 * GET /chat
   Returns 405 not allowed
 * GET /chat/<chat_id>
   Returns the last chats as they were in the DB (encrypted)
 * POST /chat/<chat_id>
   Publish a new entry in the chat. The message should contain the sender and
   the target, which could be either a group or a user.
 * PUT /chat/<chat_id>
   Creates a new chat entry.

### Database Model
Here a proposal on the database model to be used:

#### User table
Contains the following fields:

 * name (PK)

 * password (stored as sha256 hash encoded in ascii-hex)

 * picture

 * private_key

 * public_key

#### Group table
Contains the following fields:

 * group_id (PK)

 * name

 * picture

 * private_key

 * public_key

#### Chat table
Contains the following fields:

 * chat_id (PK)

 * creator (FK) 

 * creation_timestamp 

 * lastmessage_timestamp 

 * members (blob) ;//only used for secret chats

 * symetric_key (optional) ;// not sure how to use this yet

### Messages table

 * chat_id (FK)

 * message (encrypted)

 * sender (FK)

 * target (FK)


## Current Prototype
The current prototype, is monolithic, it doesn't allow multiple
requests, and it uses a non-performant relational database. The prototype
evolution will go towards this direction so that it support the desired
requirements.

The current prototype only supports a basic session handling and lays out the
idea of the data model, defines some concepts and ideas, the business logic of
the application, and the user interface. 
It has served to learn more about the possibilities of flask and to check the
viability of handling certain aspects of the application in JavaScript (i.e.
encryption, hashing, etc).

## Future Steps
The application should evolve towards the architecture described above. To
achieve this and distribute this work among different members of a virtual
team, I will organise the application in Stories. Specific tasks can be defined
by the virtual team members when implementing.

### Epics/Stories/Tasks
* Setup the python-flask skeleton for the BackEnd

* Implement the User resource as an python object. It should provide different
  methods that will be associated with each HTTP operation over that resource. 

   * Write the sqlalchmey model and database layout modeling the user (use
     sqllite for the time being)

   * Write flask method to support the PUT operation (TDD). 

      * Write flask tests (try to do all of this in a TDD fashion). These tests
        should use a dabatase mockup instead of the real one, to make them
        reliable and fast.

   * Write flask method to support the GET operation without a user id. 

      * Implement some query filters, ie: number of results, sequence, etc

   * Write flask method to support the GET operation with a user id (TDD). 

   * Write flask method to support the POST operation (TDD )

   * Write flask method to support the deletion of a user (TDD)(optional)

* Implement the Group in the same manner as proceeded with the user. Split this
  into subparts when doing it.

* Implement the Chat in the same manner as proceeded with the user. Split this
  into subparts when doing it.

* Make the backend configuratble so it can read configuration from a file (yaml?/json?)

* Create a dockerfile to handle the database service using MariaDB or postgres. 

* Connect the BackEnd service to the docker database using the configuration

  * Write some tests to verify the connection works fine, some sort of smoke tests/integration tests.

* Create a dockerfile to handle the BackEnd.

* Create a docker configuration to integrate both (dockercompose?)

* Define the protocol used to encrypt the messages: use asymmetric encryption or
  symmetric encryption with some interchange mechanism?

* Implement the key interchange mechanism, if any, into the BackEnd.

  * Make tests for it

* Implement the front-end based on the prototype. Be sure to use AJAX to access
  to the REST resources instead of going directly to the database. 

  * Write some tests using flask and fakes if possible.

  * Organise the front-end using the MVC pattern.

  * Refine the Jinja templates 

* Implement the JavaScript necessary to encrypt the messages according to the
  defined protocol.

* Find/configure a nice bootstrap template to use

* Provide a way to configure the front-end service.

* Create dockerfile to run the Fron-End, integrate with the rest of the
  system with docker compose.

* Make some UI tests, perhaps using sikuli?


### Estimation
The items educed earlier are subjected to change and they are not providing
enough information nor certainty to provide a good estimate. A good way to
handle this, would be to start with a couple of iterations, and refining and
prioritizing this backlog so that at the end the team can use relative
estimations comparing complexity. This will allow to get some educated guesses
of which could be the number of hours needed to complete the whole system. 
