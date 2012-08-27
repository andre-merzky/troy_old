
"""  
TROY: Tiered Resource Overlay
=============================

Overview:
=========

  Troy is a scheduling overlay which specifically operates on pilot systems.  In
  order to understand what Troy provides, it is helpful to discuss 'Scheduling' as
  an abstract concept, and then apply it to scheduling on pilot resources.
  
  We define the process of scheduling as follows::
  
      Assume a set of resources under control of a resource manager.  Users
      communicate the intent to utilize resources by submitting description of said
      utilization -- a workplan.  That workplan includes information about the
      required subset of resources, the kind of work planned, and any additional
      relevant or irrelevant information.
      [ MS: Is the introduction of a 'workplan' really necessary? ]
    
      The resource manager can either decline to enact the requested workplan, or to
      enact it at some point in time, on some subset of its resources.  That
      (manager internal) decision making process is called scheduling.  
    
      The scheduling process can very well be (and usually is) decentral and
      hierarchical:  a sequence of scheduling subprocesses is utilized to make the
      final enactment decision and placement.  Any one of those scheduling
      subprocesses may add additional constraints to the workplan, such as limit its
      enactment to a specific part of the over all resource set, constrain the
      co-locality of certain elements of the workplan, constrain the execution time
      and accounting method for the workplan, etc.  If any of the scheduling
      constraints contradict each other, or if the application of the constraints to
      the resource set results in an empty set, the enactment of the workplan will
      be impossible, and the scheduling request is declined [1].  Once the complete
      set of constraints pinpoints the enactment of the workplan in space and time,
      i.e. once the workplan has no free parameters, the workplan is considered to
      be 'scheduled for execution'.  
    
      Note that a complex workplan may well be split apart into smaller work units,
      which may get scheduled and enacted individually.  In those cases, a workplan
      may become partially scheduled or enacted.  In particular, parts of the
      original workplan may well become enacted while other parts are not yet
      completely scheduled.
  
  
  Troy provides means to implement one specific layer in the scheduling pipeline.
  Specifically, Troy targets to support resources managed by pilot systems
  (instances of pilot frameworks), and supports the application level scheduling
  of workplans across those pilot systems (note that this Troy level scheduling
  process may in turn consist of multiple subprocesses, i.e.  subschedulers).
  [ MS: I don't think the subschedulers add much clarity)
  Once the Troy level schedulers are done, the workplans are forwarded to the
  underlying pilot systems for further scheduling and enactment.  Any scheduler on
  Troy level may perform complete scheduling, i.e. schedule the workplan for
  execution on a specific (set of) pilot(s); or may perform partial scheduling,
  i.e. add a number of constraints which limit the scheduling options of the
  downstream pilot framework schedulers.  Troy schedulers may split up or combine
  workplans before forwarding them.
  
  The L{troy.Troy} class is the user (or application) facing component of Troy.
  Its purpose is to manage a set of pilot systems (and their pilot resources), and
  to manage a set of scheduling subprocesses which perform scheduling over the
  pilot resources, as described above.  As such, L{troy.Troy} has three distinct
  sets of methods: to manage pilot resources, to manage scheduling subprocesses,
  and to handle workplans to be scheduled on the pilot resources.
  
  
Terminology:
============
  
  For the purpose of Troy, all backend pilot frameworks are expected to implement
  the P* model of pilot abstractions [1], and to expose the Pilot API associated
  with the P* model.  P* and Pilot API have the following terminology, which is
  referenced throughout the Troy documentation::
  
      - ComputeUnitDescription:
        a workplan which describes a set of planned computational tasks.
  
      - DataUnitDescription
        a workplan which describes a set of storage resource allocations (files,
        data sets).
  
      - ComputeUnit:
        representation of an enacted (compute) workplan.
  
      - DataUnit:
        representation of an enacted (data) workplan.
  
      - ComputePilotDescription:
        a workplan which describes a ComputePilot.
  
      - DataPilotDescription:
        a workplan which describes a DataPilot.
  
      - ComputePilot:
        representation of a resource which can enact ComputeUnitDescriptions,
        managed by a pilot.
  
      - DataPilot:
        representation of a resource which can enact DataUnitDescriptions, managed
        by a pilot.
  
      - ComputePilotService:
        representation of a pilot manager which handles ComputePilots.
  
      - DataPilotService:
        representation of a pilot manager which handles DataPilots.
  
      - ComputeUnitService:
        representation of a Pilot system entity which schedules and enacts
        ComputeUnits over a set of ComputePilotServices.
  
      - DataUnitService:
        representation of a Pilot system entity which schedules and enacts
        DataUnits over a set of DataPilotServices.
  
      - ComputeDataUnitService:
        representation of a Pilot system entity which schedules and enacts
        ComputeDataUnits over a set of ComputeDataPilotServices.
  
  
  Troy's own terminology is very close to the P* and PilotAPI terminology, but
  as Troy has a different semantic and scope as P* systems, its terminology must
  necessarily differ::
  
      - Scheduler:
        Troy level manager of SchedulingAlgorithm instances.
  
      - SchedulingAlgorithm:
        Troy level sub scheduler, manager by the troy.Scheduler.
  
      - PilotFramework: 
        representation of an instance of any pilot system, exposing the
        UnitService (DataUnitService, ComputeUnitService, and
        ComputeDataUnitService) and PilotService (DataPilotService and
        ComputePilotService) semantics.
        [ MS: Does it really expose all these semantics? If so, why do we need
        a different concept? ]
  
      - ComputePilotDescription: as in P* / Pilot API
      - DataPilotDescription:    as in P* / Pilot API
      - ComputePilot:            as in P* / Pilot API
      - DataPilot:               as in P* / Pilot API
      - ComputeUnitDescription:  as in P* / Pilot API
      - DataUnitDescription:     as in P* / Pilot API
      - ComputeUnit:             as in P* / Pilot API
      - DataUnit:                as in P* / Pilot API
  
  
  [1] http://radical.rutgers.edu/publications/#pstar12
  

Hello World:
============
  
  A simple Troy application scheduling a Compute centric workplan would be (on
  'Hello World' level, some details left out for brevity)::
  [ MS: Please complete, hello world examples are by definition complete ]
  
      ----------------------------------------------------------------
      import troy
  
      # create Tiered Resource Overlay ;-)
      t = troy.Troy ()
  
      # add a Round Robin scheduling algorithm
      s = troy.Scheduler ('round_robin')
      # [ MS: This looks weird. I guess I would expect something like
      # troy.Scheduler.RoundRobin or troy.RoundRobinScheduler probably ]
      t.add_scheduler (s)
      # [ MS: Given that it is called "add", and not "select", does this mean
      # there can be multiple schedulers? ]
  
      # create two ComputePilots from a BigJob PilotFramework
      pf = troy.PilotFramework ('bigjob://')
      pf.submit_pilot ([some compute pilot description])
      pf.submit_pilot ([some compute pilot description])
      # [ MS: You think its a good idea to have one submit_pilot call for both
      # data and compute? ]
  
      # add the bigjob PF to Troy, to submit work items to
      t.add_pilot_framework (pf)
      # [ MS: And the pilot job framework will announce its capabilities to the
      # system? ]
  
      # submit a compute work item
      cu = t.submit_unit ([some compute unit description])
      # [ MS: Similar to submit pilot, good idea to have one? ]
  
      cu.wait ()     # wait 'til work is done

  
      pf.cancel ()   # terminate compute pilots and bigjob
      t.cancel ()    # terminate Troy
      ----------------------------------------------------------------
  
  The Data side of the Troy looks symmetric to the compute side.  The combination
  of data and compute pilots and work items entities allows Troy to perform
  cross-cutting scheduling and optimization, prominently compute-data
  co-scheduling.
"""


# For the sake of code organization, each API class is defined in a separate
# file.  Alas, python's module naming rules then introduce an additional
# element, that file's name, so that, for example, the ComputePilot class would
# be available as troy.compute_pilot.ComputePilot.  We thus move the symbols
# into the parent namespace, which makes them available as, for example,
# troy.ComputePilot.


##############################
#
# utility API
#
from troy.base                           import Base
from troy.config                         import _Config
from troy.state                          import State
from troy.attributes                     import Callback,  Attributes
from troy.exception                      import Exception, Error

##############################
#
# Troy API
#

# scheduler
from troy.Troy                           import Troy
from troy.scheduler                      import Scheduler

# pilot frameworks, pilot descriptions and pilots
from troy.pilot_framework                import PilotFramework

from troy.data_pilot_description         import DataPilotDescription
from troy.compute_pilot_description      import ComputePilotDescription

from troy.compute_pilot                  import ComputePilot
from troy.data_pilot                     import DataPilot

# work unit description and work units
from troy.compute_unit_description       import ComputeUnitDescription
from troy.data_unit_description          import DataUnitDescription

from troy.compute_unit                   import ComputeUnit
from troy.data_unit                      import DataUnit


# [ MS: The splitting of class:file (1:1) seems to be too rigorous and not
# really pythonesqueue, but I'll leave that up to you ]

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

