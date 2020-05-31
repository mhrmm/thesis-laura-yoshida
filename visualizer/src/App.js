
import { Tree } from 'hierplane';
import React, { Component } from 'react';
import './App.css';
import './hierplane.min.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router } from "react-router-dom";
import { Nav, Navbar, Form, FormControl, Dropdown, DropdownButton } from 'react-bootstrap';
import styled from 'styled-components';
import mainLogo from'./reedlogo.png';


const Styles = styled.div`
  .navbar { background-color: #000; }
  a, .navbar-nav, .navbar-light .nav-link {
    color: black;
    &:hover { color: #999999; }
  }
  .navbar-brand {
    font-size: 1.0em;
    color: #9FFFCB;
    &:hover { color: white; }
  }
  .form-center {
    position: absolute !important;
    left: 25%;
    right: 25%;
  }
  .active a{
    background-color: green !important;
  }
  img.resize {
    max-width:50%;
    max-height:50%;
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
    return <Tree tree={this.props.value} />;
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
    event.preventDefault();
    this.props.onSubmit(this.state.userinput);
  }

  render () {
    return (
      <Form onSubmit={this.submitHandler} onChange={this.changeHandler} className="form-center">
          <FormControl type="text" name="userinput" value={this.state.userinput}  placeholder="Enter text" className="" />
      </Form>
    );        
  }
}

class NavigationBar extends Component {
   constructor(props) {
      super(props);    
      this.state = {
        brandname: 'Constituency Parsing',
        userinput: ''
      }
   }
   
   clickHandler(model) {
     this.props.onClick(model)
     var aliases = {
        'berkeley': 'Constituency Parsing',
        'biaffine': 'Dependency Parsing',
        'allencoref': 'Coreference Resolution'
      }     
     this.setState({
       brandname: aliases[model]
     });
   }
   
   render () {
     return (
       <Styles>
        <Navbar expand="lg">           
          <Navbar.Brand href="/">
            <img height="40" src={mainLogo} alt="fireSpot"/>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav"/>
          <FormComponent onSubmit={this.props.onSubmit}/>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <div>
              <DropdownButton alignRight id="dropdown-basic-button" variant="secondary" title={this.state.brandname}>
                <Dropdown.Item as="button" onClick={() => this.clickHandler("berkeley")}>Constituency Parsing</Dropdown.Item>
                <Dropdown.Item as="button" onClick={() => this.clickHandler("biaffine")}>Dependency Parsing</Dropdown.Item>
                <Dropdown.Item as="button" onClick={() => this.clickHandler("allencoref")}>Coreference Resolution</Dropdown.Item>
              </DropdownButton>
              </div>              
            </Nav>
          </Navbar.Collapse>
        </Navbar>
       </Styles>
     )
   }
}


class App extends React.Component  {
  constructor(props) {
    super(props); 
    this.state = {
      placeholder: "Enter text",
      tree: aTree,
      model: "berkeley",
      sentence: "Green ideas sleep furiously."
    };
  }
   
  componentDidMount(sent, model) {
    document.title = "Reed NLP"
    let url;
    if(sent === undefined) {
        url = "http://127.0.0.1:5000/api/v1/translate?model=" + model + "&sent=Colorless+green+ideas+sleep+furiously+.";
    }
    else {
        url = "http://127.0.0.1:5000/api/v1/translate?model=" + model + "&sent=" + sent;
    }
    fetch(url)
      .then(results => { 
        return results.json(); 
      }).then(data => {
        data.map((payload) => this.setState({ tree: payload.parse}))
      });
  }
   
  handleSubmit(i) {
    this.setState({sentence: i})
    var sentence = i.split(" ").join("+");
    this.componentDidMount(sentence, this.state.model);
  }
  
  handleClick(m) {
    this.setState({model: m})
    var sentence = this.state.sentence.split(" ").join("+");
    this.componentDidMount(sentence, m);
  }
  
  render() {
      //alert(this.state.placeholder)
      return (
        <div>
            <Router>
            <NavigationBar onSubmit={i => this.handleSubmit(i)}  
                     onClick={model => this.handleClick(model)}                                 
                     placeholder={this.state.placeholder}
              />
            </Router>
            <TreeContainer value={this.state.tree}/>
        </div>
      );
   }
}
export default App;
document.body.style = 'background: #3C4046;';
