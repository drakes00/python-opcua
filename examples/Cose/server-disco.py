import sys
sys.path.insert(0, "../..")
import time


from opcua import ua, Server
from IPython import embed


if __name__ == "__main__":
    STATE = {}
    TRANSLATE = {}

    # add custom callback to detect attack
    def oracle(session, params):
        # Retrieve variable written and new value.
        tmp = params.NodesToWrite[0]
        varWritten = tmp.NodeId.to_string()
        valWritten = tmp.Value.Value.Value

        if (varWritten,valWritten) == (TRANSLATE["D"], False):
            # Command opens disconnector.
            if STATE[TRANSLATE["B1"]] and (STATE[TRANSLATE["B2"]] or STATE[TRANSLATE["B3"]]):
                print("alert")
        else:
            # Update state.
            STATE[varWritten] = valWritten


    # setup our server
    server = Server(oracle)
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    disco = objects.add_object(idx, "Disconnector")
    b1 = disco.add_variable(idx, "B1", True)
    b2 = disco.add_variable(idx, "B2", True)
    b3 = disco.add_variable(idx, "B3", True)
    d  = disco.add_variable(idx, "D",  True)
    TRANSLATE["B1"] = b1.get_path()[-1].nodeid.to_string()
    TRANSLATE["B2"] = b2.get_path()[-1].nodeid.to_string()
    TRANSLATE["B3"] = b3.get_path()[-1].nodeid.to_string()
    TRANSLATE["D"]  = d.get_path()[-1].nodeid.to_string()
    STATE[TRANSLATE["B1"]] = True
    STATE[TRANSLATE["B2"]] = True
    STATE[TRANSLATE["B3"]] = True
    STATE[TRANSLATE["D"]]  = True
    b1.set_writable()    # Set B1 to be writable by clients
    b2.set_writable()    # Set B2 to be writable by clients
    b3.set_writable()    # Set B3 to be writable by clients
    d.set_writable()     # Set D  to be writable by clients

    # starting!
    server.start()

    try:
        #embed()
        while True:
            time.sleep(1)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
