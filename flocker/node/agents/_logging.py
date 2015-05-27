# Copyright ClusterHQ Inc.  See LICENSE file for details.

from eliot import Field, ActionType, MessageType

# Begin: Helper datastructures to log all
# IBlockDeviceAPI calls from AWS storage driver using Eliot.

# An OPERATION is a list of:
# IBlockDeviceAPI name, positional arguments, keyword arguments.
OPERATION = Field.forTypes(
    u"operation", [list],
    u"The IBlockDeviceAPI command being executed, \
    along with positional and keyword arguments.")

# ActionType used by AWS storage driver.
AWS_ACTION = ActionType(
    u"flocker:node:agents:blockdevice:aws",
    [OPERATION],
    [],
    u"An IBlockDeviceAPI command is executing using AWS storage driver.")

# Three fields to gather from EC2 response to Boto.
AWS_CODE = Field.for_types(
    "aws_code", [bytes, unicode],
    u"The error response code.")
AWS_MESSAGE = Field.for_types(
    "aws_message", [bytes, unicode],
    u"A human-readable error message given by the response.",
)
AWS_REQUEST_ID = Field.for_types(
    "aws_request_id", [bytes, unicode],
    u"The unique identifier assigned by the server for this request.",
)

# Log boto.exception.BotoEC2ResponseError, covering all errors from AWS:
# server operation rate limit exceeded, invalid server request parameters, etc.
BOTO_EC2RESPONSE_ERROR = MessageType(
    u"boto:boto_ec2response_error", [
        AWS_CODE,
        AWS_MESSAGE,
        AWS_REQUEST_ID,
    ],
)

DEVICES = Field.forTypes(
    u"devices", [list],
    u"The list of devices currently in use by the compute instance.")
NO_AVAILABLE_DEVICE = MessageType(
    u"flocker:node:agents:blockdevice:aws:devicesearch",
    [DEVICES],
)

SIZE = Field.forTypes(
    u"size", [int],
    u"The size, in bytes, of new device we are expecting to manifest \
    in the OS.")
TIME_LIMIT = Field.forTypes(
    u"time_limit", [int],
    u"Time, in seconds, waited for new device to manifest in the OS.")
NO_NEW_DEVICE_IN_OS = MessageType(
    u"flocker:node:agents:blockdevice:aws:unavailabledevice",
    [DEVICES, SIZE, TIME_LIMIT],
    u"No new block device manifested in the OS since given base device list.",
)

# End: Helper datastructures used by AWS storage driver.
