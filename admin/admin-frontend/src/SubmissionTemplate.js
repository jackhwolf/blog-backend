import React from 'react'
import ReactDOM from 'react-dom'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'

class SubmissionTemplate extends React.Component {

    constructor(props) {
        super(props)
        this.myForm = React.createRef()
        this.title = React.createRef()
        this.desc = React.createRef() 
        this.tags = React.createRef() 
        this.token = React.createRef() 
        this.path = React.createRef()
    }

    async submit() {
        var remoteresp = await this.myPost(
            'http://13.56.250.168/v1/blogpost',
            {
                title: this.title.current.value,
                desc: this.desc.current.value,
                tags: this.tags.current.value
            }
        )
        console.log(remoteresp)
        var localresp = await this.myPost(
            'http://127.0.0.1:5000/v1/movepost',
            {
                postid: remoteresp.uploadkey,
                localpath: this.path.current.value 
            }
        )
        console.log(localresp)
        ReactDOM.findDOMNode(this.myForm).reset();
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
                <Card bg="primary" text="white" style={{ width: '30rem', height: '36.5rem' }}>
                    <Card.Header>Gimme that new post</Card.Header>
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
                </Card>
            </>
        )
    }
}


export default SubmissionTemplate