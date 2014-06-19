# Copyright 2012 Rackspace Hosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# > twistd -n -y examples/tracing-server.tac
#

import os
import sys

from twisted.application import internet, service

from twisted.web import server, static

from tryfer.http import TracingWrapperResource
from tryfer.tracers import push_tracer, RawZipkinTracer, ZipkinTracer, DebugTracer, EndAnnotationTracer
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from scrivener import ScribeClient

# Add the debug tracer.
client = ScribeClient(TCP4ClientEndpoint(reactor,'127.0.0.1', 9410))
push_tracer(EndAnnotationTracer(ZipkinTracer(client)))

# Create an application
application = service.Application("tracing-server")

# Create a TCPServer listening on port 8080 serving the current directory
# using twisted.web and our TracingWrapperResource.
#
# We can pass it a service name argument to be used in the endpoints
# attached to our annotations.
service = internet.TCPServer(
    8088,
    server.Site(
        TracingWrapperResource(
            static.File(os.getcwd()),
            service_name='tracing-server-example')))

service.setServiceParent(application)
