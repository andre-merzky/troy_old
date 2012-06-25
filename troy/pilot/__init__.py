
"""

Troy is an implementation of the Pilot API, which is an interface to pilot
abstractions.  Most prominently, pilot abstractions cover PilotJobs, a well
known mechanism for application level job management, which is usually employed
for HTC type applications on HPC type resources (amongst others).  Another pilot
abstraction is PilotData, which, in a similar fashion as PilotJobs, decouples
system level and application level data management.  Finally, the Pilot API
exposes the ability to handle Compute and Data workloads concurrently, by
interleaving PilotJobs and PilotData concepts.

The main concepts and classes exposed by the Compute part of the API are:

    - L{ComputePilot} (CP): 
          a pilot job, which can execute some compute workload (L{ComputeUnit})

    - L{ComputePilotService} (CPS): 
          a factory (service) which can create L{ComputePilot}s according to some
          specification

    - L{ComputeUnit} (CU): 
          a work item executed on a L{ComputePilot}

    - L{ComputeUnitService} (CUS):
          a service which can map L{ComputeUnit} requests to a set of
          L{ComputePilot}s

The L{ComputeUnitService} is what the application will mostly work with: it takes
care of proper work item distribution, and will in fact enact the applications
compute workload.  The set of L{ComputePilot}s available to the CUS can be changed
during the application's runtime.  A simple example (on 'Hello World' level)
would be (some details left out for brevity)::

    ----------------------------------------------------------------
    import troy

    # create on ComputePilot from a BigJob ComputePilotservice
    cps = troy,pilot.ComputePilotService ('bigjob://')
    cp  = cps.create_pilot ([some compute pilot description])

    # create a work unit service with one ComputePilot resource, to submit work
    # items to
    cus = troy.pilot.ComputeUnitService ()
    cus.add_pilot (cp)

    # submit some compute work item
    cu  = cus.submit ([some work unit description])

    cu.wait ()     # wait 'til work is done

    cp.cancel  ()  # terminate compute pilots
    cus.cancel ()  # terminate cus
    ----------------------------------------------------------------


The Data side of the Pilot API looks symmetric to the compute side.  The exposed
classes are:

    - L{DataPilot} (DP): 
          a pilot store, which can manage some data workload (L{DataUnit})

    - L{DataPilotService} (DPS): 
          a factory (service) which can create L{DataPilot}s according to some
          specification

    - L{DataUnit} (DU): 
          a data item managed by a L{DataPilot}

    - L{DataUnitService} (DUS):
          a service which can map L{DataUnit} requests to a set of
          L{DataPilot}s


Finally, the API exposes two additional classes:

    - L{ComputeDataUnit} (CDU):
          a combination of data and compute workload which the application
          requests to be handled via the Pilot API

    - L{ComputeDataUnitService} (CDUS)
          a service which can map CDUs to a set of L{ComputePilot}s and
          L{DataPilot}s.

So, the CDUS combines the abilities of the CUS and DUS, but at the same time
allows for a richer semantics -- for example, the CDUS will transparently be
able to support data-compute-colocation for the requested data-compute workload
units.

"""

# For the sake of code organization, each API class is defined in a separate
# file.  Alas, python's module naming rules then introduce an additional
# element, that file's name, so that, for example, the ComputePilot class would
# be available as troy.pilot.compute_pilot.ComputePilot.  We thus move the
# symbols into the parent namespace, which makes them available as, for example,
# troy.pilot.ComputePilot.
#
# FIXME: consider separate name spaces, like compute.Pilot and data.Pilot, etc.



from troy.pilot.state                          import State                        
from troy.pilot.callback                       import Callback                     
from troy.pilot.exception                      import TroyException, Error

from troy.pilot.compute_pilot_description      import ComputePilotDescription    
from troy.pilot.compute_pilot                  import ComputePilot                
from troy.pilot.compute_pilot_service          import ComputePilotService        
from troy.pilot.compute_unit_description       import ComputeUnitDescription     
from troy.pilot.compute_unit                   import ComputeUnit                 
from troy.pilot.compute_unit_service           import ComputeUnitService         


from troy.pilot.data_pilot_description         import DataPilotDescription       
from troy.pilot.data_pilot                     import DataPilot                   
from troy.pilot.data_pilot_service             import DataPilotService           
from troy.pilot.data_unit_description          import DataUnitDescription        
from troy.pilot.data_unit                      import DataUnit                    
from troy.pilot.data_unit_service              import DataUnitService            

from troy.pilot.compute_data_unit_description  import ComputeDataUnitDescription
from troy.pilot.compute_data_unit              import ComputeDataUnit            
from troy.pilot.compute_data_unit_service      import ComputeDataUnitService    

from troy.pilot.compute_scheduler              import ComputeScheduler_
from troy.pilot.data_scheduler                 import DataScheduler_
from troy.pilot.compute_data_scheduler         import ComputeDataScheduler_


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

