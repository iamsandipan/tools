'''
Created on Aug 11, 2017

@author: sandipan.chakrabarti
'''
import boto3 
import sys

def getecrimage(reponame):
        try:
            response = ecrclient.list_images(
                registryId='091036132616',
                repositoryName=reponame,
                maxResults=1,
                filter={
                    'tagStatus': 'TAGGED'
                }
            )
            return '091036132616.dkr.ecr.us-east-1.amazonaws.com/' + response['imageIds'][0]['imageTag']
        except Exception as ex:
            return ex
        
        
def deployImage(servicename, clustername):
        
        try:
            response = ecsclient.describe_services(
                       cluster=clustername,
                       services=[
                            servicename
                        ]
            )
            service =  response['services'][0]
            
            taskDefStr = service['taskDefinition']
            servicename= service['serviceName']
            desiredCount = service['desiredCount']
            deploymentConfig = service['deploymentConfiguration']
            
            
            existingtaskdef = ecsclient.describe_task_definition(
                taskDefinition=taskDefStr
            )['taskDefinition']
            
            
            taskfamily = existingtaskdef['family']
            tasknetworkmode = existingtaskdef['networkMode']
            containerDefinitions = existingtaskdef['containerDefinitions']
            # containerDefinitions[0]['image'] = containerDefinitions[0]['image']
            taskvolumes = existingtaskdef['volumes']
            taskplacementConstraints = existingtaskdef['placementConstraints']
            defresponse = ecsclient.register_task_definition(family=taskfamily,
                                                             networkMode=tasknetworkmode,
                                                             containerDefinitions=containerDefinitions,
                                                             volumes=taskvolumes,
                                                             placementConstraints=taskplacementConstraints)
            
            newTaskDefArn = defresponse['taskDefinition']['taskDefinitionArn']
            print(newTaskDefArn)
            response = ecsclient.update_service(
                                                cluster=clustername,
                                                service=servicename,
                                                desiredCount=desiredCount,
                                                taskDefinition=newTaskDefArn,
                                                deploymentConfiguration=deploymentConfig
                                            )
            print (response)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    env = sys.argv[1]
    serviceid = sys.argv[2]
    clusterid = sys.argv[3]
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    ecsclient = session.client('ecs')
    ecrclient = session.client('ecr')
    image = getecrimage(serviceid)
    deployImage(serviceid, clusterid)
    #getecrimage('pss-vault-imagedetection', 'PSS-VAULT-DEV-CLUSTER')
 
