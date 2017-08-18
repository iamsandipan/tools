'''
Created on Aug 11, 2017

@author: sandipan.chakrabarti
'''
import boto3 
import sys
import datetime
import time
repo_service_map = {
    'pss-vault-fileupdate':'pss-vault-fileupdate',
    'pss-vault-imagedetection':'pss-vault-imagedetection',
    'pss-vault-fileworker':'pss-vault-fileworker',
    'pss-vault-atagservice':'pss-vault-atagservice',
    'pss-vault-authenticationservice-int':'pss-vault-authenticationservice',
    'pss-vault-identifyme':'pss-vault-identifyme',
    'pss-vault-filedelete-wrk':'pss-vault-filedelete',
    'pss-vault-configservice':'pss-vault-configservice',
    'pss-vault-searchservice-ext':'pss-vault-searchservice',
    'pss-vault-reportingservice-int':'pss-vault-reportingservice',
    'pss-vault-filecleanupworker':'pss-vault-filecleanupworker',
    'pss-vault-reportingservice-ext':'pss-vault-reportingservice',
    'pss-vault-accountservice-ext':'pss-vault-accountservice',
    'pss-vault-droppedenrollment':'pss-vault-droppedenrollment',
    'pss-vault-bellprovisioning':'pss-vault-bellprovisioning',
    'pss-vault-fileservice':'pss-vault-fileservice',
    'pss-vault-authenticationservice-ext':'pss-vault-authenticationservice',
    'pss-vault-dataapi':'pss-vault-dataapi',
    'pss-vault-accountservice-int':'pss-vault-accountservice',
    'pss-vault-searchservice-int':'pss-vault-searchservice',
    'pss-vault-imagedetection-wrk':'pss-vault-imagedetection',
    'pss-vault-imagedetectionbacklog-worker':'pss-vault-imagedetectionbacklog-worker',
    'pss-vault-sprintprovisioning':'pss-vault-sprintprovisioning'
}


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
            
            
                
            latestpush= int(time.mktime((datetime.datetime.today() - datetime.timedelta(days=int(30))).timetuple()))

            latestImage = ''
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
            containerDefinitions[0]['image'] = image
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

    image = getecrimage(repo_service_map[serviceid])
    deployImage(serviceid, clusterid, image)

 
