
import { Tree } from 'hierplane';
import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import './hierplane.min.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Nav, Navbar, Form, FormControl } from 'react-bootstrap';
import styled from 'styled-components';
const Styles = styled.div`
  .navbar { background-color: #222; }
  a, .navbar-nav, .navbar-light .nav-link {
    color: #9FFFCB;
    &:hover { color: white; }
  }
  .navbar-brand {
    font-size: 1.4em;
    color: #9FFFCB;
    &:hover { color: white; }
  }
  .form-center {
    position: absolute !important;
    left: 25%;
    right: 25%;
  }
`;


const aTree =  {  
    "nodeTypeToStyle": {
        "other": [
            "color0"
        ],
        "event": [
            "color1",
            "strong"
        ],
        "entity": [
            "color2"
        ],
        "detail": [
            "color3"
        ],
        "sequence": [
            "seq"
        ],
        "reference": [
            "placeholder"
        ]
    },
    "text": "Colorless green ideas sleep furiously .",
    "root": {
        "nodeType": "event",
        "word": "Colorless green ideas sleep furiously .",
        "link": "S",
        "children": [
            {
                "nodeType": "entity",
                "word": "Colorless green ideas",
                "link": "NP",
                "children": [
                    {
                        "nodeType": "detail",
                        "word": "Colorless",
                        "link": "JJ",
                        "spans": [
                            {
                                "start": 0,
                                "end": 9
                            }
                        ]
                    },
                    {
                        "nodeType": "detail",
                        "word": "green",
                        "link": "JJ",
                        "spans": [
                            {
                                "start": 10,
                                "end": 15
                            }
                        ]
                    },
                    {
                        "nodeType": "entity",
                        "word": "ideas",
                        "link": "NNS",
                        "spans": [
                            {
                                "start": 16,
                                "end": 21
                            }
                        ]
                    }
                ]
            },
            {
                "nodeType": "event",
                "word": "sleep furiously",
                "link": "VP",
                "children": [
                    {
                        "nodeType": "event",
                        "word": "sleep",
                        "link": "VBP",
                        "spans": [
                            {
                                "start": 22,
                                "end": 27
                            }
                        ]
                    },
                    {
                        "nodeType": "detail",
                        "word": "furiously",
                        "link": "ADVP",
                        "children": [
                            {
                                "nodeType": "detail",
                                "word": "furiously",
                                "link": "RB",
                                "spans": [
                                    {
                                        "start": 28,
                                        "end": 37
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "nodeType": "other",
                "word": ".",
                "link": ".",
                "spans": [
                    {
                        "start": 38,
                        "end": 39
                    }
                ]
            }
        ]
    }
};

class TreeContainer extends React.PureComponent {
  render() {
    return <Tree tree={aTree} />;
  }
}

class FormComponent extends Component {
   constructor(props) {
      super(props);    
    this.state = {
      userinput: ''
    }
  }
  
  changeHandler = event => {
    this.setState({
      userinput: event.target.value
    });
  }

  submitHandler = event => {
    this.props.onSubmit(this.state.userinput);
  }

  render () {
    return (
      <Form onSubmit={this.submitHandler} className="form-center">
          <FormControl type="text" name="userinput" value={this.state.userinput} onChange={this.changeHandler}  placeholder="Enter text" className="" />
      </Form>
    );        
  }
}

class NavigationBar extends Component {
   constructor(props) {
      super(props);    
      this.state = {
        userinput: ''
      }
   }
   
   render () {
     return (
       <Styles>
        <Navbar expand="lg">
          <Navbar.Brand href="/">Reed NLP</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav"/>
          <FormComponent onSubmit={this.props.onSubmit}/>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Item><Nav.Link href="/">Home</Nav.Link></Nav.Item> 
              <Nav.Item><Nav.Link href="/about">About</Nav.Link></Nav.Item>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
       </Styles>
     )
   }
}


class App extends React.Component  {
  handleSubmit(i) {
    alert(i);
  }
  
  render() {
      return (
        <div>
            <Router>
            <NavigationBar onSubmit={this.handleSubmit}                                   
                     placeholder="Enter text"
              />
            </Router>
            <TreeContainer />
        </div>
      );
   }
}
export default App;
document.body.style = 'background: #3C4046;';
