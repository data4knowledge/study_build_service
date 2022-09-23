from fastapi import FastAPI, HTTPException
from model.system import SystemOut
from model.study import Study, StudyIn, StudyList, StudyParameters
from model.study_identifier import StudyIdentifier
from model.study_design import StudyDesign
from model.activity import Activity, ActivityIn
from model.study_epoch import StudyEpoch, StudyEpochIn
from model.study_data import StudyData, StudyDataIn
from model.encounter import Encounter, EncounterIn, EncounterLink
from model.workflow import Workflow, WorkflowIn
from model.workflow_item import WorkflowItem, WorkflowItemIn
from utility.service_environment import ServiceEnvironment
from typing import List

VERSION = "0.1"
SYSTEM_NAME = "d4k Study Build Microservice"

app = FastAPI(
  title = SYSTEM_NAME,
  description = "A microservice to handle Study Builds in a Neo4j database.",
  version = VERSION
 # ,openapi_tags=tags_metadata
)

@app.get("/", 
  summary="Get system and version",
  description="Returns the microservice system details and the version running.", 
  response_model=SystemOut)
@app.get("/v1", 
  summary="Get system and version",
  description="Returns the microservice system details and the version running.", 
  response_model=SystemOut)
async def read_root():
  return SystemOut(**{ 'system_name': SYSTEM_NAME, 'version': VERSION, 'environment': ServiceEnvironment().environment() })

@app.get("/v1/studies", 
  summary="List of studies",
  description="Provide a list of all studies.",
  status_code=200,
  response_model=StudyList)
async def list_studies(page: int = 0, size: int = 0, filter: str=""):
  return StudyList.list(page, size, filter)

@app.post("/v1/studies", 
  summary="Create a new study",
  description="Creates a study. If succesful the uuid of the created resource is returned.",
  status_code=201,
  response_model=str)
async def create_study(study: StudyIn):
  result = Study.create(study.identifier, study.title)
  if result == None:
    raise HTTPException(status_code=409, detail="Trying to create a duplicate study")
  else:
    return result

@app.delete("/v1/studies/{uuid}", 
  summary="Delete a study",
  description="Deletes the specified study.",
  status_code=204)
async def delete_study(uuid: str):
  result = Study.delete(uuid)

@app.get("/v1/studies/{uuid}", 
  summary="Get a study",
  description="Provides the detail for a specified study.",
  response_model=Study)
async def get_study(uuid: str):
  study = Study.find_full(uuid)
  if study == None:
    raise HTTPException(status_code=404, detail="The requested study cannot be found")
  else:
    return study

@app.get("/v1/studies/{uuid}/studyDesigns", 
  summary="Get the study designs for a study",
  description="Provides a list of uuids for te study designs that exisit for a specified study.",
  response_model=List[StudyDesign])
async def get_study_designs(uuid: str):
  study = Study.find(uuid)
  if study == None:
    raise HTTPException(status_code=404, detail="The requested study cannot be found")
  else:
    return study.study_designs()

@app.get("/v1/studies/{uuid}/parameters", 
  summary="Get the study parameters (type, phase) for a study",
  description="Provides a dictionary of the study parameters that exisit for a specified study.",
  response_model=StudyParameters)
async def get_study_parameters(uuid: str):
  study = Study.find(uuid)
  if study == None:
    raise HTTPException(status_code=404, detail="The requested study cannot be found")
  else:
    return study.study_parameters()

@app.get("/v1/studies/{uuid}/identifiers", 
  summary="Get the study identifiers for a study",
  description="Provides a dictionary of the study identifiers that exisit for a specified study.",
  response_model=List[StudyIdentifier])
async def get_study_identifiers(uuid: str):
  study = Study.find(uuid)
  if study == None:
    raise HTTPException(status_code=404, detail="The requested study cannot be found")
  else:
    return study.study_identifiers()

@app.get("/v1/studyDesigns/{uuid}/studyEpochs", 
  summary="Get the epochs for a study design",
  description="Provides a list of uuids for the epochs that exisit for a specified study.",
  response_model=List[StudyEpoch])
async def get_study_design_epochs(uuid: str):
  study_design = StudyDesign.find(uuid)
  if study_design == None:
    raise HTTPException(status_code=404, detail="The requested study design cannot be found")
  else:
    return study_design.epochs()

@app.get("/v1/studyDesigns/{uuid}/workflows", 
  summary="Get the workflows for a study design",
  description="Provides a list of uuids for the workflows that exisit for a specified study.",
  response_model=List[Workflow])
async def get_study_design_epochs(uuid: str):
  study_design = StudyDesign.find(uuid)
  if study_design == None:
    raise HTTPException(status_code=404, detail="The requested study design cannot be found")
  else:
    return study_design.workflows()

@app.get("/v1/studyDesigns/{uuid}/soa", 
  summary="Get the SoA for a study design",
  description="Provides the Schedule of Activities for a given study design.",
  response_model=list)
async def get_study_design_soa(uuid: str):
  study_design = StudyDesign.find(uuid)
  if study_design == None:
    raise HTTPException(status_code=404, detail="The requested study design cannot be found")
  else:
    return study_design.soa()

@app.get("/v1/studyDesigns/{uuid}/dataContract", 
  summary="Get the data contract for a study design",
  description="Provides the data contract for a given study design.",
  response_model=list)
async def get_study_design_soa(uuid: str):
  study_design = StudyDesign.find(uuid)
  if study_design == None:
    raise HTTPException(status_code=404, detail="The requested study design cannot be found")
  else:
    return study_design.data_contract()

@app.post("/v1/studyDesigns/{uuid}/studyEpochs", 
  summary="Create a new epoch within a study",
  description="Creates an epoch. The epoch is added to the end of the list of epochs for the specified study.",
  status_code=201,
  response_model=str)
async def create_epoch(uuid: str, epoch: StudyEpochIn):
  print("A1")
  result = StudyEpoch.create(uuid, epoch.name, epoch.description)
  if result == None:
    raise HTTPException(status_code=409, detail="Trying to create a duplicate epoch within the study")
  else:
    return result

@app.post("/v1/studyDesigns/{uuid}/activities", 
  summary="Create a new activity within a study",
  description="Creates an activity. The activity is added to the end of the list of activities for the specified study.",
  status_code=201,
  response_model=str)
async def create_activity(uuid: str, activity: ActivityIn):
  result = Activity.create(uuid, activity.name, activity.description)
  if result == None:
    raise HTTPException(status_code=409, detail="Trying to create a duplicate activity within the study")
  else:
    return result

@app.post("/v1/studyDesigns/{uuid}/encounters", 
  summary="Creates a new encounter within a study design",
  description="Creates an encounter withn a study design.",
  status_code=201,
  response_model=str)
async def create_encounter(uuid: str, encounter: EncounterIn):
  result = Encounter.create(uuid, encounter.name, encounter.description)
  if result == None:
    raise HTTPException(status_code=409, detail="Trying to create a duplicate encounter within the study")
  else:
    return result

@app.post("/v1/studyDesigns/{uuid}/workflows", 
  summary="Creates a new workflow within a study design",
  description="Creates an workflow withn a study design.",
  status_code=201,
  response_model=str)
async def create_workflow(uuid: str, wf: WorkflowIn):
  result = Encounter.create(uuid, wf.name, wf.description)
  if result == None:
    raise HTTPException(status_code=409, detail="Trying to create a duplicate workflow within the study")
  else:
    return result

@app.post("/v1/activities/{uuid}/studyData", 
  summary="Creates a new study data item within an activity",
  description="Creates an an item of study data.",
  status_code=201,
  response_model=str)
async def create_study_data(uuid: str, study_data: StudyDataIn):
  activity = Activity.find(uuid)
  result = activity.add_study_data(study_data.name, study_data.description, study_data.link)
  return result

@app.put("/v1/studyEpochs/{uuid}/encounters", 
  summary="Links an encounter with an epoch",
  description="Creates an link between an epoch and an encounter.",
  status_code=201,
  response_model=str)
async def link_epoch_and_encounter(uuid: str, encounter: EncounterLink):
  epoch = StudyEpoch.find(uuid)
  result = epoch.add_encounter(encounter.uuid)
  return result

@app.post("/v1/workflows/{uuid}/workflowItems", 
  summary="Creates an encounter and an activity to a workflow",
  description="Creates an encounter and an activity to a workflow",
  status_code=201,
  response_model=str)
async def create_workflow_item(uuid: str, wfi: WorkflowItemIn):
  workflow = Workflow.find(uuid)
  result = workflow.add_workflow_item(wfi.description, wfi.encounter_uuid, wfi.activity_uuid)
  return result
