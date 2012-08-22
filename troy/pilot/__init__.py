
"""

Troy is an implementation of the Pilot API, which is an interface to pilot
abstractions.  Most prominently, pilot abstractions cover PilotJobs, a well
known mechanism for application level job management, which is usually employed
for HTC type applications on HPC type resources (amongst others).  Another pilot
abstraction is PilotData, which, in a similar fashion as PilotJobs, decouples
system level and application level data management.

The Pilot API exposes the ability to handle Compute and Data workloads
concurrently, by interleaving PilotJobs and PilotData concepts.

The main concepts and classes of the API are:

    - L{ComputePilot} (CP) / L{DataPilot} (DP):
      a pilot, which manages a (compute or data) resource slice for the
      application

    - L{ComputePilotFramework} (CPF) / L{DataPilotFramework} (DPF):
      creates and manages pilots, according to application specified resource
      requirements.  Also, 'submit_xxx_unit()' methods accept work descriptions
      of L{ComputeUnit}s and L{DataUnit}s to be executed on its pilots.

    - L{ComputeUnitDescription} (CUD) / L{DataUnitDescription} (DUD) /
      L{ComputeDataUnitDescription} (CDUD) :
      describes a piece of (compute or data or combination thereof) workload, to
      be managed by a (set of) pilot(s).

    - L{ComputeUnit} (CU) / L{DataUnit} (DU) / L{ComputeDataUnit} (CDU):
      represents an instance of a piece of (compute or data) workload, which was
      created according to a L{ComputeUnitDescription} / L{DataUnitDescription}
      / L{ComputeDataUnitDescription}

    - L{ComputeUnitService} (CUS) / DataUnitService (DUS) /
      ComputeDataUnitService (CDUS):
      an application level scheduler which can instantiate L{ComputeUnit}s,
      L{DataUnit}s and L{ComputeDataUnit}s on a set of L{ComputePilotFramework}s
      and L{DataPilotFramework}s, and their pilots.

The UnitService's is what the application will mostly work with: it takes care
of proper work item distribution, and will in fact enact the applications
workload.  The set of pilots available to the UnitService can be changed during
the application's runtime.  A simple (compute) example on 'Hello World' level
would be (some details left out for brevity)::

    ----------------------------------------------------------------
    import troy

    # create on ComputePilot from a BigJob ComputePilotFramework
    cpf = troy,pilot.ComputePilotFramework ('bigjob://')
    cpf.submit_pilot ([some compute pilot description])

    # create a work unit service with one ComputePilot resource, to submit work
    # items to
    cus = troy.pilot.ComputeUnitService ()
    cus.add_pilot_framework (cpf)

    # submit a compute work item
    cu = cus.submit_unit ([some compute unit description])

    cu.wait ()     # wait 'til work is done

    cus.cancel ()  # terminate cus
    cpf.cancel ()  # terminate compute pilots
    ----------------------------------------------------------------

The Data side of the Pilot API looks symmetric to the compute side.  The
combination of data and compute focused entities in the ComputeData-type classes
allows Troy to perform cross-cutting scheduling and optimization, prominently
compute-data co-scheduling.

"""

#
# For the sake of code organization, each API class is defined in a separate
# file.  Alas, python's module naming rules then introduce an additional
# element, that file's name, so that, for example, the ComputePilot class would
# be available as troy.pilot.compute_pilot.ComputePilot.  We thus move the
# symbols into the parent namespace, which makes them available as, for example,
# troy.pilot.ComputePilot.
#
# FIXME: consider separate name spaces, like compute.Pilot and data.Pilot, etc.



from troy.pilot.config                         import Config_
from troy.pilot.state                          import State
from troy.pilot.attributes                     import Callback, Attributes
from troy.pilot.exception                      import TroyException, Error

from troy.pilot.compute_pilot_description      import ComputePilotDescription
from troy.pilot.compute_pilot                  import ComputePilot
from troy.pilot.compute_pilot_framework        import ComputePilotFramework
from troy.pilot.compute_unit_description       import ComputeUnitDescription
from troy.pilot.compute_unit                   import ComputeUnit
from troy.pilot.compute_unit_service           import ComputeUnitService

from troy.pilot.data_pilot_description         import DataPilotDescription
from troy.pilot.data_pilot                     import DataPilot
from troy.pilot.data_pilot_framework           import DataPilotFramework
from troy.pilot.data_unit_description          import DataUnitDescription
from troy.pilot.data_unit                      import DataUnit
from troy.pilot.data_unit_service              import DataUnitService

from troy.pilot.compute_data_unit_description  import ComputeDataUnitDescription
from troy.pilot.compute_data_unit              import ComputeDataUnit
from troy.pilot.compute_data_unit_service      import ComputeDataUnitService

from troy.pilot.compute_scheduler              import ComputeScheduler
from troy.pilot.data_scheduler                 import DataScheduler
from troy.pilot.compute_data_scheduler         import ComputeDataScheduler


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

