
TROY -- Tiered Resource Overlay (*)
--------------------------------------------------------------------------------

What is Troy?
--------------------------------------------------------------------------------

 As the acronym suggests, Troy provides an abstract view onto computational
 resources.  In particular, Troy supports application level management of
 resources, and supports application level scheduling of tasks on those
 resources.

 More specifically, Troy is a framework to utilize pilot systems, such as
 PilotJobs or PilotData frameworks.  In very general terms, pilot systems
 allocate system resource slices and hand control over those resource slices to
 the application layer.  For example, pilot jobs are genuine jobs queued on
 compute resources, which, once getting instantiated, act as container jobs, 
 executing arbitrary application defined computing tasks (compute units).

 Using pilot systems, applications can limit the impact of queue waiting times
 and other scheduling artifacts onto their internal workflow.  For example,
 a pilot job is passing the system queue only once, incurring only one unit of
 queue waiting time, while an arbitrary number of compute units can be executed
 on that pilot without any additional system level wait time.  

 Further, applications can utilize application level information for task
 scheduling.  For example, the application level logic enacting the compute
 units in the container pilot can ensure that logically depending units are
 executed in order -- which is not at all trivial or even possible with system
 level schedulers.


How does Troy compare to other pilot frameworks?
--------------------------------------------------------------------------------

 First, Troy is not a pilot framework itself, but instead *interfaces* to other
 pilot frameworks.  Adding that additional layer of indirection has
 3 (interrelated) benefits:

  * Interoperability:
    It is relatively difficult to use 2 different pilot systems in the same
    application, even if they *conceptually* provide very similar semantics.
    Troy simplifies that, by providing a common API to different backend pilot
    systems.

  * Application level scheduling:
    Pilot systems are used by applications to perform scheduling decisions on
    application level, across the resource slices acquired by the pilots.  Troy
    gives a *generic* way to implement a variety of scheduling algorithms,
    independent on the underlying pilot system, and also working across multiple
    pilot backends.

  * Separation of concerns:
    Many pilot systems are (more or less) tightly interwoven with the specific
    distributed infrastructure they operate on.  As such, they are well able to
    use system level information to perform basic application level scheduling,
    such as load balancing, or error recovery.  On the other hand, scheduling
    decisions which rely on purely application level information are not easily
    provided in a generic way -- while some pilot systems support simple DAG
    level task dependencies, none (we know of) goes beyond that to support
    cyclic DGs.  Troy allows to implement the required scheduling logic close 
    to the application level, while being able to utilize the pilot system
    lower-level scheduling capabilities.


How does Troy interact with other pilot frameworks?
--------------------------------------------------------------------------------

 Pilot systems all follow a very similar inherent architecture, or model, the
 'P* model of pilot abstractions' [1].  Troy's API ('Pilot API') exposes the
 application facing components of the very same P* model, and thus can be
 semantically mapped very well to arbitrary pilot systems (which are interfaced
 to by adaptors).  Some pilot systems provide the same Pilot API as Troy, and
 adaptors are then relatively trivial to write.  For other systems, Troy's
 Pilot API need to be mapped to the system's native API.


How does Troy interact with DIANE[2]?
--------------------------------------------------------------------------------

 DIANE is a pilot job application framework, developed at CERN.  




How does Troy support application level scheduling?
--------------------------------------------------------------------------------

 Whenever a work unit is submitted on Troy level, the Troy implementation will
 route that request to an internal scheduler class.  That scheduler uses again
 an adaptor mechanism to talk to different scheduler implementations -- which
 can be provided by the application.  
 
 Those scheduler adaptors have different means of obtaining the required
 information required to make scheduling decisions:

  - inspect the pilots they operate on (load, locality, type, ...)
  - inspect the backend pilot system   (load, type, ...)
  - inspect the internal troy state
  - obtain out-of band system information (contact information services etc.)
  - use application specific and/or scheduler specific information sources
  - query the application for additional information

 The last item is at the moment not implemented, as the other information
 channels seem to suffice for all use cases so far -- it will be provided once
 new application use cases require it.

 Note that a very simple adaptor could simply forward scheduling requests to the
 lower layer pilot systems -- thus rendering Troy semantically void.




--------------------------------------------------------------------------------

(*) For those not familiar with Greek sagas: the name relates to the siege of
Troy, and the 'Trojan Horse': after 10 years siege of Troy, the Greeks came up
with a ruse: they pulled back, just leaving a large wooden horse.  The Trojans
celebrated the end of the siege, and displayed the horse at the city's center
square, as token of their victory.  The cunning Greeks though had hidden some
soldiers in the horse, which, late at night, when the (by then mostly drunk)
Trojans slept), opened the gates to let the Greek army into the city.  We hope
that the similarity between the Trojan Horse and Pilot jobs is obvious ;-)


[1]  http://dl.acm.org/citation.cfm?id=2287094&dl=ACM&coll=DL&CFID=118451532&CFTOKEN=85218786
[2]  https://twiki.cern.ch/twiki/bin/view/ArdaGrid/DIANETutorial

DAG: Directed Acyclic  Graph
DG:  Directed Graph (can be cyclic)

  
