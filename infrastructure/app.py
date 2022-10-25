from aws_cdk import core

from stacks.cicd_stack import CiCdStack
from stacks.networking_stack import NetworkingStack
from stacks.serving_stack import ServingStack

app = core.App()

shared_context = app.node.try_get_context('arn:aws:codestar-connections:us-east-1:255219863677:connection/61d68dc7-2b2b-4495-963e-ccdbec7dad13')
#shared_context = app.node.try_get_context('shared_context')

cdk_environment = core.Environment(
    region=shared_context['us-east-1'],
    account=shared_context['255219863677'])

cicd = CiCdStack(scope=app,
                 id='classifier-cicd-stack',
                 env=cdk_environment,
                 shared_context=shared_context)

networking = NetworkingStack(app, 'classifier-networking-stack', env=cdk_environment)

serving = ServingStack(app,
                       id='classifier-serving-stack',
                       vpc=networking.vpc,
                       repository=cicd.ecr_repository,
                       env=cdk_environment,
                       shared_context=shared_context)

app.synth()
