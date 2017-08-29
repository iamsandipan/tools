'''
Created on Aug 25, 2017

@author: sandipan.chakrabarti
'''

import boto3
import json
import pprint
client = boto3.client('cloudwatch')

def getKeyOrNone(key, mapobj):
    if key in mapobj:
        return mapobj[key]
    else:
        return ' '
    
    
if __name__ == "__main__":
    alarmnames=[
            'PSS-VAULT-PP-UPLOADED-FILES-S3EVENTS-QUEUE-DECREASE',
            'awsec2-ECS-PSS-VAULT-SQA-CLUSTER-High-CPU-Utilization-Down',
            'pss-vault-scaledown-alarm',
            'pss-vault-sprint-enrollment-worker',
            'pss-vault-imagedetection-low-cpu-scaling-alarm',
            'pss-vault-authenticationservice-ext-low-cpu-scaling-alarm',
            'pss-vault-fileservice-low-cpu-scaling-alarm',
            'pss-vault-imagedetection-high-cpu-scaling-alarm',
            'pss-vault-reportingservice-int-high-cpu-scaling-alarm',
            'pss-vault-configservice-high-cpu-scaling-alarm',
            'pss-vault-fileworker-high-cpu-scaling-alarm',
            'pss-vault-authenticationservice-ext-high-cpu-scaling-alarm',
            'pss-vault-accountservice-int-low-cpu-scaling-alarm',
            'pss-vault-configservice-low-cpu-scaling-alarm',
            'pss-vault-accountservice-ext-high-cpu-scaling-alarm',
            'pss-vault-droppedenrollment-high-cpu-scaling-alarm',
            'pss-vault-reportingservice-ext-high-cpu-scaling-alarm',
            'pss-vault-fileworker-low-cpu-scaling-alarm',
            'pss-vault-reportingservice-ext-low-cpu-scaling-alarm',
            'pss-vault-droppedenrollment-low-cpu-scaling-alarm',
            'pss-vault-accountservice-ext-low-cpu-scaling-alarm',
            'pss-vault-reportingservice-int-low-cpu-scaling-alarm',
            'pss-vault-accountservice-int-high-cpu-scaling-alarm',
            'pss-vault-fileupdate-high-cpu-scaling-alarm',
            'pss-vault-sprintprovisioning-low-cpu-scaling-alarm',
            'pss-vault-filedelete-high-cpu-scaling-alarm',
            'pss-vault-authenticationservice-int-low-cpu-scaling-alarm',
            'pss-vault-fileupdate-low-cpu-scaling-alarm',
            'pss-vault-filedelete-low-cpu-scaling-alarm',
            'pss-vault-sprintprovisioning-high-cpu-scaling-alarm',
            'awsec2-ECS-PSS-VAULT-SQA-CLUSTER-CPU-Utilization',
            'pss-vault-bellprovisioning-low-cpu-scaling-alarm',
            'pss-vault-authenticationservice-int-high-cpu-scaling-alarm',
            'pss-vault-bellprovisioning-high-cpu-scaling-alarm',
            'pss-vault-fileservice-high-cpu-scaling-alarm',
            'pss-vault-identifyme-low-cpu-scaling-alarm',
            'pss-vault-identifyme-high-cpu-scaling-alarm',
            'pss-vault-searchservice-int-low-cpu-scaling-alarm',
            'pss-vault-searchservice-ext-low-cpu-scaling-alarm',
            'pss-vault-searchservice-ext-high-cpu-scaling-alarm',
            'pss-vault-searchservice-int-high-cpu-scaling-alarm',
            'PSS-VAULT-QA-UPLOADED-FILES-S3EVENTS-QUEUE-SIZE-ALARM',
            'PSS-VAULT-PP-UPLOADED-FILES-S3EVENTS-QUEUE-INCREASE'
        ]
    
    
    for alarm in alarmnames:
        
        response = client.describe_alarms(
            AlarmNames=[
               alarm 
            ]
        )
        alarmdetail = response['MetricAlarms'][0]
        print(getKeyOrNone('OKActions', alarmdetail))
        print(getKeyOrNone('AlarmActions', alarmdetail))
        print(getKeyOrNone('InsufficientDataActions', alarmdetail))


        alarm_name = getKeyOrNone('AlarmName', alarmdetail)   
        alarm_desc = getKeyOrNone('AlarmDescription', alarmdetail)
        alarm_action_enabled = getKeyOrNone('ActionsEnabled', alarmdetail)
        ok_actions = getKeyOrNone('OKActions', alarmdetail)
        ok_actions.append('arn:aws:sns:us-east-1:330932647836:pss-vault-cloudwatch-topic')
        alarm_actions = getKeyOrNone('AlarmActions', alarmdetail)
        alarm_actions.append('arn:aws:sns:us-east-1:330932647836:pss-vault-cloudwatch-topic')
        insuff_data_action = getKeyOrNone('InsufficientDataActions', alarmdetail)
        insuff_data_action.append('arn:aws:sns:us-east-1:330932647836:pss-vault-cloudwatch-topic')
    
        metric_name = getKeyOrNone('MetricName', alarmdetail)
        name_space = getKeyOrNone('Namespace', alarmdetail)
        statistic = getKeyOrNone('Statistic', alarmdetail)
        extended_statistic = getKeyOrNone('ExtendedStatistic', alarmdetail)
        diamentions = getKeyOrNone('Dimensions', alarmdetail)
        period = getKeyOrNone('Period', alarmdetail)
        unit = getKeyOrNone('Unit', alarmdetail)
        if unit == ' ':
            unit = 'Seconds'
        eval_period = getKeyOrNone('EvaluationPeriods', alarmdetail)
        threshold = getKeyOrNone('Threshold', alarmdetail)
        comparisonOperator = getKeyOrNone('ComparisonOperator', alarmdetail)
        treatMissingData = getKeyOrNone('TreatMissingData', alarmdetail)
        evaluateLowSampleCountPercentile = getKeyOrNone('EvaluateLowSampleCountPercentile', alarmdetail)

        '''
        try:
            update_alarm_config = client.put_metric_alarm(
                
                AlarmName=alarm_name,
                AlarmDescription=alarm_desc,
                ActionsEnabled=alarm_action_enabled,
                OKActions=ok_actions,
                AlarmActions=alarm_actions,
                InsufficientDataActions=insuff_data_action,
                MetricName=metric_name,
                Namespace=name_space,
                Statistic=statistic,
                Dimensions=diamentions,
                Period=period,
                Unit=unit,
                EvaluationPeriods=eval_period,
                Threshold=threshold,
                ComparisonOperator=comparisonOperator,
                TreatMissingData=treatMissingData,
                EvaluateLowSampleCountPercentile = evaluateLowSampleCountPercentile
            );
        except Exception as ex:
            print(ex)
        
        print(update_alarm_config)
        '''
