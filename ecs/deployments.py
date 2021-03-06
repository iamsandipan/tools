'''
Created on Aug 11, 2017

@author: sandipan.chakrabarti
'''
import boto3 
import sys
import datetime
import time

def getecrimage(reponame):
        try:
            images = []
            response = ecrclient.describe_images(
                registryId='091036132616',
                repositoryName=reponame,
                filter={
                    'tagStatus': 'TAGGED'
                }
            )
            images = response['imageDetails']
            
            nexttoken = None
            if('NextToken' in response):
                nexttoken = response['NextToken']

            while(nexttoken != None):
                response = ecrclient.describe_images(
                    registryId='091036132616',
                    repositoryName=reponame,
                    filter={
                        'tagStatus': 'TAGGED'
                    },
                    NextToken=nexttoken
                )
                if('NextToken' in response):
                    nexttoken = response['NextToken']
                else:
                    nexttoken = None  
                images.append(response['imageDetails'])
            
            
                
            latestpush= int(time.mktime( images[0]["imagePushedAt"].timetuple()))

            latestImage = images[0]
            for img in images:
                pushed_time = int(time.mktime( img["imagePushedAt"].timetuple()))
                if pushed_time > latestpush:
                    latestpush = pushed_time
                    latestImage = img
             
            return '091036132616.dkr.ecr.us-east-1.amazonaws.com/' + reponame +':'+ latestImage['imageTags'][0]
        except Exception as ex:
            print(ex)
            return ex
        
        
def deployImage(servicename, clustername, image):
        print('Will Try Updating Service With Image' + image)
        try:
            response = ecsclient.describe_services(
                       cluster=clustername,
                       services=[
                            servicename
                        ]
            )
            if 'services' in response:
                service =  response['services'][0]
            else:
                raise Exception('Service Not Present')
            
            if 'taskDefinition' in service:    
                taskDefStr = service['taskDefinition']
            else:
                raise Exception('TaskDefinition Not Present')

            if 'serviceName' in service:
                servicename= service['serviceName']
            else:
                raise Exception('Service Name Not Present')

            if 'desiredCount' in service:
                desiredCount = service['desiredCount']
            else:
                desiredCount = 1
            
            if 'deploymentConfiguration' in service:    
                deploymentConfig = service['deploymentConfiguration']
            else:
                raise Exception('DeploymentConfiguration Name Not Present')

            
            existingtaskdef = ecsclient.describe_task_definition(
                taskDefinition=taskDefStr
            )['taskDefinition']
            
            if 'family' in existingtaskdef:
                taskfamily = existingtaskdef['family']
            else:
                raise Exception('TaskDefinition Family Name Not Present')
  
            
            if 'networkMode' in existingtaskdef:
                tasknetworkmode = existingtaskdef['networkMode']
                print(tasknetworkmode)
            else:
                tasknetworkmode = 'bridge'    
            
            if 'containerDefinitions' in existingtaskdef:
                containerDefinitions = existingtaskdef['containerDefinitions']
                containerDefinitions[0]['image'] = image
            else:
                raise Exception('containerDefinitions  Not Present in TaskDefinitions')

            
            if 'volumes' in existingtaskdef:
                taskvolumes = existingtaskdef['volumes']

            if 'placementConstraints' in existingtaskdef:
                taskplacementConstraints = existingtaskdef['placementConstraints']
            
            print('Registering Task Definition')
            defresponse = ecsclient.register_task_definition(family=taskfamily,
                                                             networkMode=tasknetworkmode,
                                                             containerDefinitions=containerDefinitions,
                                                             volumes=taskvolumes,
                                                             placementConstraints=taskplacementConstraints)
            
            newTaskDefArn = defresponse['taskDefinition']['taskDefinitionArn']
            print('Updating Service ....' + servicename  + ' for taskfamily :' + taskfamily)
            response = ecsclient.update_service(
                                                cluster=clustername,
                                                service=servicename,
                                                desiredCount=desiredCount,
                                                taskDefinition=newTaskDefArn,
                                                deploymentConfiguration=deploymentConfig
                                            )
            print (response['ResponseMetadata'])
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    env = sys.argv[1]
    serviceid = sys.argv[2]
    clusterid = sys.argv[3]
    repositoryname = sys.argv[4]
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    ecsclient = session.client('ecs')
    ecrclient = session.client('ecr')

    image = getecrimage(repositoryname)
    deployImage(serviceid, clusterid, image)

 
