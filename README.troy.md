
TODO AM: this document needs to be merged into the project home page.

TROY -- Tiered Resource Overlay 
================================================================================

What is Troy[1]?
--------------------------------------------------------------------------------

 As the acronym expansion suggests, Troy provides an abstract view onto
 computational resources.  In particular, Troy supports application level
 management of resources, and supports application level scheduling of tasks on
 those resources.

 Troy is a framework to utilize pilot systems, such as PilotJobs or PilotData
 frameworks.  In very general terms, pilot systems allocate system resource
 slices and hand control over those resource slices to the application layer.
 For example, pilot jobs are genuine jobs queued on compute resources, which,
 once getting instantiated, act as container jobs, executing arbitrary
 application defined computing tasks (compute units).

 Using pilot systems, applications can limit the impact of system level resource
 management artifacts onto their internal workflow.  For example, a pilot job is
 passing the system queue only once, incurring only one unit of queue waiting
 time, while an arbitrary number of compute units can be executed on that pilot
 without any additional system level wait time.  

 Further, pilot systems simplify the utilization of application level
 information for task scheduling.  For example, the application level logic
 enacting the compute units in the container pilot can ensure that logically
 depending units are executed in order -- which is not at all trivial or even
 possible with system level schedulers.  Troy supports the implementation of
 such application level schedulers.


How does Troy compare to other pilot frameworks?
--------------------------------------------------------------------------------

 First, Troy is not a pilot framework itself, but instead *interfaces* to other
 pilot frameworks.  Adding that additional layer of indirection has
 3 (interrelated) benefits:

  * Interoperability:
    It is relatively difficult to use different pilot systems in the same
    application, even if they *conceptually* provide very similar semantics.
    Troy simplifies that, by providing a common API to different backend pilot
    systems.

  * Application level scheduling:
    Pilot systems are used by applications to perform scheduling decisions on
    application level, across the resource slices acquired by the pilots.  Troy
    provides a generic way to implement a variety of scheduling algorithms,
    independent on the underlying pilot system, which can schedule work unites
    across multiple pilot backends.

  * Separation of concerns:
    Many pilot systems are (more or less) tightly interwoven with the specific
    distributed infrastructure they operate on.  As such, they are well able to
    use system level information to perform basic application level scheduling,
    such as load balancing, or error recovery.  On the other hand, scheduling
    decisions which rely on purely application level information are not easily
    provided in a generic way -- while some pilot systems support simple DAG
    level task dependencies, or task affinities, few go beyond that to
    generically support application level scheduling constraints.  Troy allows
    to implement such scheduling logic close to the application level, while
    still being able to utilize the pilot system lower-level scheduling
    capabilities.


How does Troy interact with other pilot frameworks?
--------------------------------------------------------------------------------

 Pilot systems mostly follow a very similar inherent architecture, or model, the
 'P* model of pilot abstractions' [2].  Troy's API ('Pilot API') exposes the
 application facing components of the very same P* model, and thus maps
 semantically very well to arbitrary pilot systems (which are interfaced to by
 adaptors).  Some pilot systems such as BigJob may provide the same Pilot API as
 Troy, and adaptors are then relatively trivial to write.  For other systems,
 Troy's Pilot API need to be mapped to the system's native API.

 The following classes in Troy are interfacing to the backend pilot systems:

   * ComputePilotService
   * ComputePilot
   * ComputeUnit

   * DataPilotService
   * DataPilot
   * DataUnit

   * ComputeDataUnit


How does Troy support application level scheduling?
--------------------------------------------------------------------------------

 Additionally to the exposed P* model entities, Troy also exposes additional
 objects (work unit services), which render the application level scheduling
 layer.  Those objects are *not* mapped to backend pilot system entities, but
 provided within the Troy framework.
 
 Whenever a work unit is submitted on Troy level, to one of the work unit
 services, the Troy implementation will route that request to an internal
 scheduler class.  Troy application can either explicitly provide a scheduling
 routine to Troy, for each work unit service instance, or it can set a Troy
 level scheduler (adaptor) for them.  Either way, the high level scheduling is
 thus managed independently from the underlying Pilot framework(s).
 
 The scheduler routines or adaptors have different means of obtaining the
 required information required to make scheduling decisions:

   * inspect the pilots they operate on (load, locality, type, ...)
   * inspect the backend pilot system, i.e. the pilot service classes)
   * inspect the internal troy state
   * obtain out-of band system information (information services etc.)
   * use application specific and/or scheduler specific information sources

 Note that a very simple scheduler could simply forward scheduling requests to
 the lower layer pilot systems -- thus rendering Troy semantically void.

 The following classes in Troy are not interfacing to the backend pilot systems,
 but are used for Troy's application level scheduling capabilities:

   * ComputeUnitService
   * DataUnitService
   * ComputeDataUnitService
  
 Additionally, the following interfaces are provided to the application, to
 implement application level scheduling:

   * ComputeUnitScheduler
   * DataUnitScheduler
   * ComputeDataUnitScheduler


What other classes exist in Troy?
--------------------------------------------------------------------------------

 The following classes in Troy are essentially Python dictionaries, and are used
 to describe resource requirements and workload properties:

   * ComputePilotDescription
   * DataPilotDescription
   * ComputeDataPilotDescription

   * ComputeUnitDescription
   * DataUnitDescription
   * ComputeDataUnitDescription
  
 A number of utility classes and interfaces are provided, whose use is explained
 in the API documentation in more detail:

   * State      (enum like)
   * Attributes (interface base for the *Description classes)
   * Callback   (base class used for monitoring state changes etc)
   * Config     (Troy configuration dictionary)
   * Exception  (set of error codes and exception class)
   
 All of the above classes are in the troy.pilot namespace.  There are additional
 classes in the troy.engine, troy.interface and troy.adaptors namespace -- those
 are not intended for application level usage, but rather for adaptor
 implementors, and are described in some detail on the Troy wiki pages[4].


How does Troy interact with BigJob[3]?
--------------------------------------------------------------------------------

 FIXME


How does Troy interact with DIANE[4]?
--------------------------------------------------------------------------------

 FIXME





--------------------------------------------------------------------------------

[1] For those not familiar with Greek sagas: the name relates to the siege of
    Troy, and the 'Trojan Horse': after 10 years siege of Troy, the Greeks came
    up with a ruse: they pulled back, just leaving a large wooden horse at the
    gate of Troy.  The Trojans celebrated the end of the siege, and displayed
    the horse at the city's center square, as token of their victory.  The
    cunning Greeks though had hidden some soldiers in the horse, which, late at
    night, when the (by then mostly drunk) Trojans slept, opened the gates to
    let the Greek army into the city.  We hope that the similarity between the
    Trojan Horse and Pilot jobs is obvious ;-)

[2] http://arxiv.org/abs/1207.6644v1                               <br>
[3] https://github.com/saga-project/BigJob/                        <br>
[4] https://twiki.cern.ch/twiki/bin/view/ArdaGrid/DIANETutorial    <br>
[5] https://github.com/saga-project/troy/wiki/                     <br>
