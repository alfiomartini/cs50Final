class Modal{
    constructor(message){
        this.setModal(message);
    }

    setModal(message){
        this._message = message;
        this._modal = `<!-- Trigger the modal with a button -->
        <button type="button" class="btn btn-primary" id="myBtn" hidden>Open Modal</button>
        <!-- The Modal -->
        <div class="modal fade" id="myModal">
            <div class="modal-dialog">
                <div class="modal-content text-dark">
                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h4 class="modal-title">Error</h4>
                        <button type="button" class="close" data-dismiss="modal">×</button>
                    </div>
                    
                    <!-- Modal body -->
                    <div class="modal-body">
                    ${this._message}
                    </div>
                    
                    <!-- Modal footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>`;
    }
     
    getModal(){
        return this._modal;
    }

    getMessage(){
        return this._message;
    }

    setMessage(message){
        this._message = message;
    }

    fireModal(){
        $("#myBtn").click(function(){
            $("#myModal").modal();
            });
        let event = new Event("click");
        let myBtn = document.getElementById('myBtn');
        myBtn.dispatchEvent(event);
    }
}