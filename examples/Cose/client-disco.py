import sys
sys.path.insert(0, "../..")

##  Paquet Sequence
#   Packet# | Seq Num   | Command
#   ------------------------------------------
#   1       | 1         | OpenSecureChannel
#   2       | 2         | CreateSession
#   3       | 3         | ActivateSession
#   --------|-----------|---------------------
#   4       | 4         | Browse, B1
#   5       | 5         | Browse, B2
#   6       | 6         | Browse, B3
#   7       | 7         | Browse, D
#   --------|-----------|---------------------
#                     WRAP
#   --------|-----------|---------------------
#   8       | 1         | Write, B1, False
#   9       | 2         | Write, B2, False
#   10      | 3         | Write, B3, False
#   11      | 4         | Write, D,  False


# W,D,F == 4 (premier après wrap) == 12

from opcua import Client
from IPython import embed


if __name__ == "__main__":

    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        #print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        #print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        b1 = root.get_child(["0:Objects", "2:Disconnector", "2:B1"])
        b2 = root.get_child(["0:Objects", "2:Disconnector", "2:B2"])
        b3 = root.get_child(["0:Objects", "2:Disconnector", "2:B3"])
        d  = root.get_child(["0:Objects", "2:Disconnector", "2:D"])

        d.get_value()

        b1.get_value()
        b3.get_value()

        #b1.set_value(False)
        #b3.set_value(False)
        d.set_value(False)

        #embed()

    finally:
        client.disconnect()
