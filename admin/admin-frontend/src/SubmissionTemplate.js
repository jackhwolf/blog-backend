import React from 'react'
import ReactDOM from 'react-dom'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'

class SubmissionTemplate extends React.Component {

    constructor(props) {
        super(props)
        this.big = '38.5rem'
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
            trigger: 1
        }
        this.myForm = React.createRef()
        this.title = React.createRef()
        this.desc = React.createRef() 
        this.tags = React.createRef() 
        this.token = React.createRef() 
        this.path = React.createRef()
    }

    async submit() {
        var remoteresp = await this.myPost(
            'http://13.56.250.168/v1/blogpost', {
                title: this.title.current.value,
                desc: this.desc.current.value,
                tags: this.tags.current.value,
            }
        )
        console.log("[SubmissionTemplate.submit] remote response:")
        console.log(remoteresp)
        this.changeDisplay()
        var localresp = await this.myPost(
            'http://127.0.0.1:5000/v1/submitpost', {
                postid: remoteresp.uploadkey,
                localpath: this.path.current.value
            }
        )
        console.log("[SubmissionTemplate.submit] local response:")
        console.log(localresp)
        this.setState({localresp: localresp})
        ReactDOM.findDOMNode(this.myForm).reset();
    }

    // this might not do anything
    refresh() {
        this.setState({
            trigger: this.state.trigger * -1
        })
    }

    // change the card that is displayed
    changeDisplay() {
        this.setState({
            submitStyle: { display: this.state.resultStyle.display },
            resultStyle: { display: this.state.submitStyle.display },
            height: this.state.height === this.big ? this.little : this.big,
            cardVar: this.state.cardVar === this.varA ? this.varB : this.varA
        })
    }

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
                <Card bg={this.state.cardVar} text="white" style={{width: '30rem', height: this.state.height}}>
                    <div style={this.state.submitStyle}>
                        <Card.Header style={{fontSize: 'xx-large'}}>Gimme that new post</Card.Header>
                        <Form id='myForm'
                            className="form"
                            ref={form => this.myForm = form}
                            style={{margin: '15px'}}>

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
                                <Form.Control type="tags" placeholder="Enter post tags" ref={this.tags}/>
                            </Form.Group>

                            <Form.Group controlId="formToken">
                                <Form.Label>Token check</Form.Label>
                                <Form.Control type="token" placeholder="Enter your admin token" ref={this.token}/>
                            </Form.Group>

                            <Form.Group controlId="formPath">
                                <Form.Label>Path on local</Form.Label>
                                <Form.Control type="path" placeholder="Enter absolute path to post file on local" ref={this.path} />
                            </Form.Group>

                            <Button variant="danger" onClick={() => this.submit()}>
                                Submit
                            </Button >
                        </Form>
                    </div>
                    <div style={this.state.resultStyle}>
                        <Card.Header style={{ fontSize: 'xx-large' }}>Check post status</Card.Header>
                        <Card.Text style={this.state.ctStyle}>
                            Status: <Card.Text style={{ fontSize: 'x-large' }}>{this.state.localresp === undefined ? "Pending" : this.state.localresp.status}</Card.Text>
                        </Card.Text>
                        <Button style={this.state.btnStyle} variant="secondary" onClick={() => this.refresh()}>
                            refresh
                        </Button>
                        <Button style={this.state.btnStyle} variant="primary" onClick={() => this.changeDisplay()}>
                            again
                        </Button>
                    </div>
                </Card>
            </>
        )
    }
}


export default SubmissionTemplate