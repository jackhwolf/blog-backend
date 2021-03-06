import React from 'react'
import ReactDOM from 'react-dom'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'

const base = '/home/twilight/py/mywebsite/admin/staging/'

class SubmissionTemplate extends React.Component {

    constructor(props) {
        super(props)
        this.big = '43.5rem'
        this.little = '15.5rem'
        this.varA = 'primary'
        this.varB = 'info'
        this.state = {
            submitStyle: { display: undefined },
            resultStyle: { display: 'none' },
            ctStyle: { padding: '15px', fontSize: 'large'},
            btnStyle: { padding: '5px', margin: '10px', width: '5rem', height: '3rem'}, 
            height: this.big,
            cardVar: this.varA,
            trigger: 1,
            status: "Pending"
        }
        this.myForm = React.createRef()
        this.title = React.createRef()
        this.desc = React.createRef() 
        this.tags = React.createRef() 
        this.media = React.createRef() 
        this.token = React.createRef() 
        this.path = React.createRef()
    }

    async submit() {
        // submit post to remote server to add to DynamoDB
        var remoteresp = await this.myPost(
            'http://13.56.250.168/v1/blogpost', {
                title: this.title.current.value,
                desc: this.desc.current.value,
                tags: this.tags.current.value,
            }
        )
        console.log("[SubmissionTemplate.submit] remote response:")
        console.log(remoteresp)
        // show user status of post
        this.changeDisplay()
        // submit post to local server to move into repo and redeploy
        var localresp = await this.myPost(
            'http://127.0.0.1:5000/v1/submitpost', {
                postid: remoteresp.uploadkey,
                localbase: base,
                localpath: this.path.current.value,
                mediapaths: this.media.current.value
            }
        )
        console.log("[SubmissionTemplate.submit] local response:")
        console.log(localresp)
        // give user result
        this.setState({localresp: localresp, status: localresp.status})
        ReactDOM.findDOMNode(this.myForm).reset();
    }

    // this might not do anything
    refresh() {
        this.setState({
            trigger: this.state.trigger * -1
        })
    }

    // change the card that is displayed
    changeDisplay(isAgain) {
        this.setState({
            submitStyle: { display: this.state.resultStyle.display },
            resultStyle: { display: this.state.submitStyle.display },
            height: this.state.height === this.big ? this.little : this.big,
            cardVar: this.state.cardVar === this.varA ? this.varB : this.varA
        })
        if (isAgain !== undefined) {
            this.setState({status: "Pending"})
        }
    }

    // helper method to POST to url w/ given body
    async myPost(url, body) {
        var resp = await fetch(url, {
            method: 'POST',
            headers: {
                'token': this.token.current.value,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        }).then(r => r.json())
        return resp
    }

    render() {
        return (
            <>
                <Card bg={this.state.cardVar} text="white" style={{width: '40rem', height: this.state.height}}>
                    <div style={this.state.submitStyle}>
                        <Card.Header style={{fontSize: 'xx-large'}}>Gimme that new post</Card.Header>
                        <Form id='myForm'
                            className="form"
                            ref={form => this.myForm = form}
                            style={{margin: '10px'}}>

                            <Form.Group controlId="formTitle">
                                <Form.Label>Post title</Form.Label>
                                <Form.Control type="title" placeholder="Enter post title" ref={this.title}/>
                            </Form.Group>

                            <Form.Group controlId="formDesc">
                                <Form.Label>Post description</Form.Label>
                                <Form.Control as="textarea" rows="3" type="desc" placeholder="Enter post description" ref={this.desc}/>
                            </Form.Group>

                            <Form.Group controlId="formTags">
                                <Form.Label>Post tags, separated by commas</Form.Label>
                                <Form.Control type="tags" placeholder="Enter post tags" ref={this.tags} />
                            </Form.Group>

                            <Form.Group controlId="formMedia">
                                <Form.Label>Assoc. media files, separated by commas</Form.Label>
                                <Form.Control type="media" placeholder="Enter media file paths" ref={this.media} />
                            </Form.Group>

                            <Form.Group controlId="formPath">
                                <Form.Label>Relative path on local (from /home/twilight/admin/staging/)</Form.Label>
                                <Form.Control type="path" placeholder="Enter rel. path to post file on local" ref={this.path} />
                            </Form.Group>

                            <Form.Group controlId="formToken">
                                <Form.Label>Token check</Form.Label>
                                <Form.Control type="password" placeholder="Enter your admin token" ref={this.token} />
                            </Form.Group>

                            <Button variant="danger" onClick={() => this.submit()}>
                                Submit
                            </Button >
                        </Form>
                    </div>
                    <div style={this.state.resultStyle}>
                        <Card.Header style={{ fontSize: 'xx-large' }}>Check post status</Card.Header>
                        <Card.Text style={this.state.ctStyle}>
                            Status: <Card.Text style={{ fontSize: 'x-large' }}>{this.state.status}</Card.Text>
                        </Card.Text>
                        <Button style={this.state.btnStyle} variant="secondary" onClick={() => this.refresh()}>
                            refresh
                        </Button>
                        <Button style={this.state.btnStyle} variant="primary" onClick={() => this.changeDisplay(true)}>
                            again
                        </Button>
                    </div>
                </Card>
            </>
        )
    }
}


export default SubmissionTemplate